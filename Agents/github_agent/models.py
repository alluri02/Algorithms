"""
Data models for GitHub Issues AI Agent.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class IssueData(BaseModel):
    """Model representing a GitHub issue."""
    
    number: int = Field(..., description="Issue number")
    title: str = Field(..., description="Issue title")
    body: Optional[str] = Field(None, description="Issue body/description")
    author: str = Field(..., description="Issue author username")
    labels: List[str] = Field(default_factory=list, description="Issue labels")
    assignees: List[str] = Field(
        default_factory=list, description="Current assignees"
    )
    state: str = Field(..., description="Issue state (open/closed)")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    url: str = Field(..., description="Issue URL")
    comments_count: int = Field(0, description="Number of comments")


class SummaryResult(BaseModel):
    """Model for AI-generated issue summary."""
    
    issue_number: int = Field(..., description="Issue number")
    summary: str = Field(..., description="AI-generated summary")
    key_points: List[str] = Field(
        default_factory=list, description="Key points extracted"
    )
    sentiment: str = Field(..., description="Sentiment analysis result")
    priority: str = Field(..., description="Suggested priority level")
    category: str = Field(..., description="Issue category")
    processing_time: float = Field(..., description="Processing time in seconds")
    model_used: str = Field(..., description="AI model used for processing")


class AssignmentRule(BaseModel):
    """Model for owner assignment rules."""
    
    name: str = Field(..., description="Rule name")
    keywords: List[str] = Field(
        default_factory=list, description="Keywords to match"
    )
    labels: List[str] = Field(
        default_factory=list, description="Labels to match"
    )
    owners: List[str] = Field(..., description="Potential owners")
    priority: int = Field(1, description="Rule priority (higher = more important)")
    conditions: Optional[Dict[str, Any]] = Field(
        None, description="Additional conditions"
    )


class AssignmentResult(BaseModel):
    """Model for owner assignment result."""
    
    issue_number: int = Field(..., description="Issue number")
    assigned_owner: Optional[str] = Field(None, description="Assigned owner")
    confidence_score: float = Field(..., description="Assignment confidence (0-1)")
    reasoning: str = Field(..., description="Assignment reasoning")
    matched_rules: List[str] = Field(
        default_factory=list, description="Rules that matched"
    )
    alternative_owners: List[str] = Field(
        default_factory=list, description="Alternative owner suggestions"
    )
    processing_time: float = Field(..., description="Processing time in seconds")


class ProcessingStats(BaseModel):
    """Model for processing statistics."""
    
    total_issues: int = Field(0, description="Total issues processed")
    successful_summaries: int = Field(0, description="Successful summaries")
    successful_assignments: int = Field(0, description="Successful assignments")
    failed_operations: int = Field(0, description="Failed operations")
    processing_time: float = Field(0.0, description="Total processing time")
    average_processing_time: float = Field(
        0.0, description="Average time per issue"
    )
    start_time: datetime = Field(
        default_factory=datetime.now, description="Processing start time"
    )
    end_time: Optional[datetime] = Field(None, description="Processing end time")
