"""
Main GitHub Issues AI Agent class.
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from github import Github
from openai import AsyncOpenAI
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from .config import Settings, get_settings
from .models import (
    IssueData, SummaryResult, AssignmentResult, 
    ProcessingStats, AssignmentRule
)
from .github_connector import GitHubConnector
from .summarizer import IssueSummarizer
from .owner_assigner import OwnerAssigner
from .utils import setup_logging


class GitHubIssueAgent:
    """
    Main AI agent for processing GitHub issues.
    
    Handles issue summarization and owner assignment using
    OpenAI API, LangChain tools, and GitHub API integration.
    """
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize the GitHub Issue Agent."""
        self.settings = settings or get_settings()
        self.logger = setup_logging(self.settings.log_level)
        
        # Initialize components
        self.github_connector = GitHubConnector(self.settings)
        self.summarizer = IssueSummarizer(self.settings)
        self.owner_assigner = OwnerAssigner(self.settings)
        
        # Processing statistics
        self.stats = ProcessingStats()
        
        self.logger.info("GitHub Issue Agent initialized successfully")
    
    async def process_issue(self, issue_number: int) -> Dict[str, Any]:
        """
        Process a single issue: summarize and assign owner.
        
        Args:
            issue_number: GitHub issue number
            
        Returns:
            Dictionary containing processing results
        """
        start_time = time.time()
        
        try:
            # Fetch issue data
            issue_data = await self.github_connector.get_issue(issue_number)
            if not issue_data:
                raise ValueError(f"Issue #{issue_number} not found")
            
            self.logger.info(f"Processing issue #{issue_number}: {issue_data.title}")
            
            # Generate summary
            summary_result = await self.summarizer.summarize_issue(issue_data)
            
            # Assign owner
            assignment_result = await self.owner_assigner.assign_owner(
                issue_data, summary_result
            )
            
            # Update GitHub issue if not dry run
            if not self.settings.enable_dry_run and assignment_result.assigned_owner:
                await self.github_connector.assign_issue(
                    issue_number, assignment_result.assigned_owner
                )
            
            # Update statistics
            self.stats.total_issues += 1
            self.stats.successful_summaries += 1
            if assignment_result.assigned_owner:
                self.stats.successful_assignments += 1
            
            processing_time = time.time() - start_time
            
            result = {
                "issue_number": issue_number,
                "issue_data": issue_data,
                "summary": summary_result,
                "assignment": assignment_result,
                "processing_time": processing_time,
                "success": True
            }
            
            self.logger.info(
                f"Successfully processed issue #{issue_number} in "
                f"{processing_time:.2f}s"
            )
            
            return result
            
        except Exception as e:
            self.stats.failed_operations += 1
            self.logger.error(f"Failed to process issue #{issue_number}: {e}")
            
            return {
                "issue_number": issue_number,
                "error": str(e),
                "processing_time": time.time() - start_time,
                "success": False
            }
    
    async def process_multiple_issues(
        self, issue_numbers: List[int]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Process multiple issues concurrently.
        
        Args:
            issue_numbers: List of GitHub issue numbers
            
        Returns:
            Dictionary mapping issue numbers to results
        """
        semaphore = asyncio.Semaphore(self.settings.max_concurrent_requests)
        
        async def process_with_semaphore(issue_number: int):
            async with semaphore:
                return await self.process_issue(issue_number)
        
        tasks = [
            process_with_semaphore(issue_num) for issue_num in issue_numbers
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            issue_numbers[i]: (
                result if not isinstance(result, Exception) 
                else {"error": str(result), "success": False}
            )
            for i, result in enumerate(results)
        }
    
    async def process_all_open_issues(self) -> Dict[int, Dict[str, Any]]:
        """
        Process all open issues in the repository.
        
        Returns:
            Dictionary mapping issue numbers to results
        """
        self.logger.info("Fetching all open issues...")
        open_issues = await self.github_connector.get_open_issues()
        
        if not open_issues:
            self.logger.info("No open issues found")
            return {}
        
        issue_numbers = [issue.number for issue in open_issues]
        self.logger.info(f"Found {len(issue_numbers)} open issues to process")
        
        return await self.process_multiple_issues(issue_numbers)
    
    async def summarize_issue(self, issue_number: int) -> str:
        """
        Generate AI summary for a specific issue.
        
        Args:
            issue_number: GitHub issue number
            
        Returns:
            AI-generated summary text
        """
        issue_data = await self.github_connector.get_issue(issue_number)
        if not issue_data:
            raise ValueError(f"Issue #{issue_number} not found")
        
        summary_result = await self.summarizer.summarize_issue(issue_data)
        return summary_result.summary
    
    async def assign_owner(self, issue_number: int) -> Optional[str]:
        """
        Assign appropriate owner to a specific issue.
        
        Args:
            issue_number: GitHub issue number
            
        Returns:
            Assigned owner username or None
        """
        issue_data = await self.github_connector.get_issue(issue_number)
        if not issue_data:
            raise ValueError(f"Issue #{issue_number} not found")
        
        # Generate summary first for better assignment
        summary_result = await self.summarizer.summarize_issue(issue_data)
        assignment_result = await self.owner_assigner.assign_owner(
            issue_data, summary_result
        )
        
        # Update GitHub issue if not dry run
        if not self.settings.enable_dry_run and assignment_result.assigned_owner:
            await self.github_connector.assign_issue(
                issue_number, assignment_result.assigned_owner
            )
        
        return assignment_result.assigned_owner
    
    def get_processing_stats(self) -> ProcessingStats:
        """Get current processing statistics."""
        self.stats.end_time = datetime.now()
        
        if self.stats.total_issues > 0:
            total_time = (
                self.stats.end_time - self.stats.start_time
            ).total_seconds()
            self.stats.processing_time = total_time
            self.stats.average_processing_time = (
                total_time / self.stats.total_issues
            )
        
        return self.stats
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all components."""
        health_status = {
            "agent": "healthy",
            "github_connector": "unknown",
            "summarizer": "unknown", 
            "owner_assigner": "unknown",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Check GitHub connection
            await self.github_connector.health_check()
            health_status["github_connector"] = "healthy"
        except Exception as e:
            health_status["github_connector"] = f"unhealthy: {e}"
        
        try:
            # Check OpenAI connection
            await self.summarizer.health_check()
            health_status["summarizer"] = "healthy"
        except Exception as e:
            health_status["summarizer"] = f"unhealthy: {e}"
        
        try:
            # Check assignment rules
            await self.owner_assigner.health_check()
            health_status["owner_assigner"] = "healthy"
        except Exception as e:
            health_status["owner_assigner"] = f"unhealthy: {e}"
        
        return health_status
