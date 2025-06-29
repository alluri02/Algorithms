"""
Issue summarization using OpenAI API and LangChain.
"""

import time
from typing import List

from openai import AsyncOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from .config import Settings
from .models import IssueData, SummaryResult


class IssueSummarizer:
    """Handles AI-powered issue summarization."""
    
    def __init__(self, settings: Settings):
        """Initialize the summarizer."""
        self.settings = settings
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.langchain_llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=settings.openai_temperature
        )
    
    async def summarize_issue(self, issue_data: IssueData) -> SummaryResult:
        """
        Generate AI summary of a GitHub issue.
        
        Args:
            issue_data: Issue data to summarize
            
        Returns:
            SummaryResult with summary and analysis
        """
        start_time = time.time()
        
        # Create summarization prompt
        prompt = self._create_summary_prompt(issue_data)
        
        try:
            # Use OpenAI API directly for summarization
            response = await self.openai_client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.settings.openai_max_tokens,
                temperature=self.settings.openai_temperature
            )
            
            summary_text = response.choices[0].message.content
            
            # Parse summary components
            summary_data = self._parse_summary(summary_text)
            
            processing_time = time.time() - start_time
            
            return SummaryResult(
                issue_number=issue_data.number,
                summary=summary_data.get("summary", ""),
                key_points=summary_data.get("key_points", []),
                sentiment=summary_data.get("sentiment", "neutral"),
                priority=summary_data.get("priority", "medium"),
                category=summary_data.get("category", "general"),
                processing_time=processing_time,
                model_used=self.settings.openai_model
            )
            
        except Exception as e:
            raise Exception(f"Failed to summarize issue: {e}")
    
    async def health_check(self) -> bool:
        """Check OpenAI API connectivity."""
        try:
            await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception:
            return False
    
    def _create_summary_prompt(self, issue_data: IssueData) -> str:
        """Create summarization prompt for the issue."""
        return f"""
Please analyze and summarize the following GitHub issue:

**Title:** {issue_data.title}
**Author:** {issue_data.author}
**Labels:** {', '.join(issue_data.labels) if issue_data.labels else 'None'}
**Created:** {issue_data.created_at}

**Description:**
{issue_data.body}

Please provide a structured analysis in the following format:

**SUMMARY:**
[Provide a concise 2-3 sentence summary of the issue]

**KEY_POINTS:**
- [Key point 1]
- [Key point 2]
- [Key point 3]

**SENTIMENT:**
[positive/negative/neutral]

**PRIORITY:**
[low/medium/high/critical]

**CATEGORY:**
[bug/feature/documentation/maintenance/question/other]

Focus on extracting the core problem, proposed solution, and impact.
Be concise but comprehensive.
"""
    
    def _parse_summary(self, summary_text: str) -> dict:
        """Parse structured summary response."""
        result = {
            "summary": "",
            "key_points": [],
            "sentiment": "neutral",
            "priority": "medium", 
            "category": "general"
        }
        
        lines = summary_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('**SUMMARY:**'):
                current_section = 'summary'
                continue
            elif line.startswith('**KEY_POINTS:**'):
                current_section = 'key_points'
                continue
            elif line.startswith('**SENTIMENT:**'):
                current_section = 'sentiment'
                continue
            elif line.startswith('**PRIORITY:**'):
                current_section = 'priority'
                continue
            elif line.startswith('**CATEGORY:**'):
                current_section = 'category'
                continue
            
            if current_section and line:
                if current_section == 'summary':
                    result['summary'] += line + ' '
                elif current_section == 'key_points' and line.startswith('-'):
                    result['key_points'].append(line[1:].strip())
                elif current_section in ['sentiment', 'priority', 'category']:
                    result[current_section] = line.lower()
        
        # Clean up summary
        result['summary'] = result['summary'].strip()
        
        return result
