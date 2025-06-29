# GitHub Issues AI Agent - Copilot Instructions

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Context
This is a GitHub Issues AI Agent that automatically:
- Summarizes GitHub issues using OpenAI API
- Assigns appropriate owners based on issue content and team expertise
- Uses LangChain tools for advanced text processing
- Integrates with GitHub API for issue management

## Tech Stack
- **Python 3.11+**: Core language
- **OpenAI API**: For issue summarization and intelligent analysis
- **LangChain**: For advanced text processing and AI tool orchestration
- **GitHub API (PyGithub)**: For GitHub integration
- **Pydantic**: For data validation and settings management
- **asyncio**: For asynchronous operations

## Code Guidelines
- Use async/await patterns for API calls
- Implement proper error handling and retry logic
- Follow Python type hints consistently
- Use Pydantic models for configuration and data structures
- Implement logging for debugging and monitoring
- Create modular, testable components
- Use environment variables for sensitive data (API keys)

## Key Components
- `GitHubIssueAgent`: Main agent class
- `IssueSummarizer`: OpenAI-based summarization
- `OwnerAssigner`: Logic for assigning issue owners
- `GitHubConnector`: GitHub API integration
- Configuration management and logging utilities
