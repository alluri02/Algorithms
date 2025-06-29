"""
Unit tests for GitHub Issues AI Agent.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch

from github_agent.agent import GitHubIssueAgent
from github_agent.config import Settings
from github_agent.models import IssueData, SummaryResult, AssignmentResult


class TestGitHubIssueAgent:
    """Test cases for the main GitHubIssueAgent class."""
    
    @pytest.fixture
    def mock_settings(self):
        """Create mock settings for testing."""
        return Settings(
            openai_api_key="test_key",
            github_token="test_token",
            github_owner="test_owner",
            github_repo="test_repo",
            enable_dry_run=True
        )
    
    @pytest.fixture
    def agent(self, mock_settings):
        """Create agent instance for testing."""
        with patch('github_agent.agent.GitHubConnector'), \
             patch('github_agent.agent.IssueSummarizer'), \
             patch('github_agent.agent.OwnerAssigner'):
            return GitHubIssueAgent(mock_settings)
    
    def test_agent_initialization(self, agent):
        """Test agent initializes correctly."""
        assert agent is not None
        assert agent.settings is not None
        assert agent.github_connector is not None
        assert agent.summarizer is not None
        assert agent.owner_assigner is not None
    
    @pytest.mark.asyncio
    async def test_health_check(self, agent):
        """Test health check functionality."""
        # Mock health check responses
        agent.github_connector.health_check = AsyncMock(return_value=True)
        agent.summarizer.health_check = AsyncMock(return_value=True)
        agent.owner_assigner.health_check = AsyncMock(return_value=True)
        
        health_status = await agent.health_check()
        
        assert health_status['agent'] == 'healthy'
        assert health_status['github_connector'] == 'healthy'
        assert health_status['summarizer'] == 'healthy'
        assert health_status['owner_assigner'] == 'healthy'
        assert 'timestamp' in health_status
    
    @pytest.mark.asyncio
    async def test_process_issue_success(self, agent):
        """Test successful issue processing."""
        # Mock issue data
        issue_data = IssueData(
            number=123,
            title="Test Issue",
            body="Test description",
            author="test_user",
            labels=["bug"],
            assignees=[],
            state="open",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
            url="https://github.com/test/test/issues/123",
            comments_count=0
        )
        
        summary_result = SummaryResult(
            issue_number=123,
            summary="Test summary",
            key_points=["Point 1", "Point 2"],
            sentiment="neutral",
            priority="medium",
            category="bug",
            processing_time=1.0,
            model_used="gpt-4"
        )
        
        assignment_result = AssignmentResult(
            issue_number=123,
            assigned_owner="developer1",
            confidence_score=0.85,
            reasoning="Matched bug rule",
            matched_rules=["Bug Reports"],
            alternative_owners=["developer2"],
            processing_time=0.5
        )
        
        # Mock component responses
        agent.github_connector.get_issue = AsyncMock(return_value=issue_data)
        agent.summarizer.summarize_issue = AsyncMock(return_value=summary_result)
        agent.owner_assigner.assign_owner = AsyncMock(return_value=assignment_result)
        agent.github_connector.assign_issue = AsyncMock(return_value=True)
        
        result = await agent.process_issue(123)
        
        assert result["success"] is True
        assert result["issue_number"] == 123
        assert result["summary"] == summary_result
        assert result["assignment"] == assignment_result
        assert "processing_time" in result
    
    @pytest.mark.asyncio
    async def test_process_issue_not_found(self, agent):
        """Test processing non-existent issue."""
        agent.github_connector.get_issue = AsyncMock(return_value=None)
        
        result = await agent.process_issue(999)
        
        assert result["success"] is False
        assert "error" in result
        assert "not found" in result["error"].lower()
    
    def test_get_processing_stats(self, agent):
        """Test getting processing statistics."""
        stats = agent.get_processing_stats()
        
        assert stats.total_issues == 0
        assert stats.successful_summaries == 0
        assert stats.successful_assignments == 0
        assert stats.failed_operations == 0
        assert stats.end_time is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
