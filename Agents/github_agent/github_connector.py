"""
GitHub API connector for issue management.
"""

import asyncio
from typing import List, Optional
from datetime import datetime

from github import Github
from github.Issue import Issue

from .config import Settings
from .models import IssueData


class GitHubConnector:
    """Handles GitHub API operations."""
    
    def __init__(self, settings: Settings):
        """Initialize GitHub connector."""
        self.settings = settings
        self.github = None
        self.repo = None
        self._initialized = False
    
    def _ensure_initialized(self):
        """Ensure GitHub connection is initialized."""
        if not self._initialized:
            self.github = Github(self.settings.github_token)
            self.repo = self.github.get_repo(
                f"{self.settings.github_owner}/{self.settings.github_repo}"
            )
            self._initialized = True
    
    async def get_issue(self, issue_number: int) -> Optional[IssueData]:
        """
        Fetch issue data from GitHub.
        
        Args:
            issue_number: GitHub issue number
            
        Returns:
            IssueData object or None if not found
        """
        try:
            self._ensure_initialized()
            issue = self.repo.get_issue(issue_number)
            return self._convert_issue_to_model(issue)
        except Exception as e:
            print(f"Error fetching issue #{issue_number}: {e}")
            return None
    
    async def get_open_issues(self) -> List[IssueData]:
        """
        Fetch all open issues from the repository.
        
        Returns:
            List of IssueData objects
        """
        try:
            self._ensure_initialized()
            open_issues = self.repo.get_issues(state='open')
            return [
                self._convert_issue_to_model(issue)
                for issue in open_issues
            ]
        except Exception as e:
            print(f"Error fetching open issues: {e}")
            return []
    
    async def assign_issue(self, issue_number: int, assignee: str) -> bool:
        """
        Assign an issue to a user.
        
        Args:
            issue_number: GitHub issue number
            assignee: Username to assign
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_initialized()
            issue = self.repo.get_issue(issue_number)
            issue.add_to_assignees(assignee)
            return True
        except Exception as e:
            print(f"Error assigning issue #{issue_number} to {assignee}: {e}")
            return False
    
    async def add_comment(self, issue_number: int, comment: str) -> bool:
        """
        Add a comment to an issue.
        
        Args:
            issue_number: GitHub issue number
            comment: Comment text
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_initialized()
            issue = self.repo.get_issue(issue_number)
            issue.create_comment(comment)
            return True
        except Exception as e:
            print(f"Error adding comment to issue #{issue_number}: {e}")
            return False
    
    async def health_check(self) -> bool:
        """Check GitHub API connectivity."""
        try:
            self._ensure_initialized()
            if self.github is not None:
                self.github.get_user().login
            return True
        except Exception:
            return False
            
    def check_config(self) -> bool:
        """Check if configuration is valid without connecting."""
        try:
            # Basic validation
            if (not self.settings.github_token or
                    self.settings.github_token == "your-github-token-here"):
                return False
            if (not self.settings.github_owner or
                    self.settings.github_owner == "your-github-username"):
                return False
            if (not self.settings.github_repo or
                    self.settings.github_repo == "your-repo-name"):
                return False
            return True
        except Exception:
            return False
    
    def _convert_issue_to_model(self, issue: Issue) -> IssueData:
        """Convert GitHub Issue to IssueData model."""
        return IssueData(
            number=issue.number,
            title=issue.title,
            body=issue.body or "",
            author=issue.user.login,
            labels=[label.name for label in issue.labels],
            assignees=[assignee.login for assignee in issue.assignees],
            state=issue.state,
            created_at=issue.created_at,
            updated_at=issue.updated_at,
            url=issue.html_url,
            comments_count=issue.comments
        )
