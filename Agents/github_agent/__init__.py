"""
GitHub Issues AI Agent

An intelligent agent for summarizing GitHub issues and assigning owners
using OpenAI API, LangChain tools, and GitHub API integration.
"""

__version__ = "1.0.0"
__author__ = "GitHub Issues AI Agent Team"

# Import main components
try:
    from .agent import GitHubIssueAgent
    from .config import Settings, get_settings
    from .models import IssueData, AssignmentResult, SummaryResult
    
    __all__ = [
        "GitHubIssueAgent",
        "Settings", 
        "get_settings",
        "IssueData",
        "AssignmentResult",
        "SummaryResult"
    ]
except ImportError as e:
    # Handle import errors gracefully during development
    print(f"Warning: Could not import all components: {e}")
    __all__ = []
