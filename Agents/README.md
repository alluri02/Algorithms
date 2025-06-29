# GitHub Issues AI Agent

An intelligent AI agent that automatically summarizes GitHub issues and assigns appropriate owners using OpenAI API, LangChain tools, and GitHub API integration.

## 🚀 Features

- **Intelligent Issue Summarization**: Uses OpenAI GPT models to create concise, meaningful summaries of GitHub issues
- **Smart Owner Assignment**: Analyzes issue content and assigns the most appropriate team member or owner
- **LangChain Integration**: Leverages advanced text processing tools for enhanced analysis
- **GitHub API Integration**: Seamlessly works with GitHub repositories and issues
- **Async Processing**: Handles multiple issues efficiently with asynchronous operations
- **Configurable Rules**: Customizable assignment logic based on keywords, labels, and team expertise

## 🛠️ Tech Stack

- **Python 3.11+**
- **OpenAI API** - Issue summarization and intelligent analysis
- **LangChain** - Advanced text processing and AI tool orchestration  
- **GitHub API (PyGithub)** - GitHub integration
- **Pydantic** - Data validation and settings management
- **asyncio** - Asynchronous operations

## 📋 Prerequisites

- Python 3.11 or higher
- OpenAI API key
- GitHub personal access token
- Git repository access

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd github-issues-ai-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# GitHub Configuration  
GITHUB_TOKEN=your_github_token_here
GITHUB_OWNER=your_github_username_or_org
GITHUB_REPO=your_repository_name

# Agent Configuration
LOG_LEVEL=INFO
MAX_CONCURRENT_REQUESTS=5
ASSIGNMENT_RULES_FILE=config/assignment_rules.yaml
```

## 🚀 Usage

### Basic Usage

```python
from github_agent import GitHubIssueAgent

# Initialize the agent
agent = GitHubIssueAgent()

# Process a specific issue
summary = await agent.summarize_issue(issue_number=123)
assigned_owner = await agent.assign_owner(issue_number=123)

# Process all open issues
await agent.process_all_open_issues()
```

### Command Line Interface

```bash
# Process a specific issue
python -m github_agent.cli --issue 123

# Process all open issues
python -m github_agent.cli --all

# Process issues with specific labels
python -m github_agent.cli --labels "bug,enhancement"

# Dry run (no actual assignments)
python -m github_agent.cli --dry-run --all
```

## 📖 API Reference

### GitHubIssueAgent

Main agent class for processing GitHub issues.

#### Methods

- `summarize_issue(issue_number: int) -> str`: Generate AI summary of an issue
- `assign_owner(issue_number: int) -> str`: Assign appropriate owner to an issue  
- `process_all_open_issues() -> Dict[int, Dict]`: Process all open issues in the repository
- `get_issue_metrics() -> Dict`: Get processing metrics and statistics

### Configuration

The agent uses YAML configuration files for assignment rules:

```yaml
# config/assignment_rules.yaml
assignment_rules:
  - keywords: ["bug", "error", "crash"]
    labels: ["bug"]
    owners: ["developer1", "developer2"]
    
  - keywords: ["feature", "enhancement"]  
    labels: ["enhancement"]
    owners: ["product_manager", "lead_dev"]
    
  - keywords: ["documentation", "docs"]
    labels: ["documentation"]
    owners: ["tech_writer", "maintainer"]
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=github_agent

# Run specific test file
python -m pytest tests/test_agent.py -v
```

## 🔍 Logging

The agent provides comprehensive logging:

```python
import logging

# Configure logging level
logging.basicConfig(level=logging.INFO)

# Logs include:
# - API request/response details
# - Issue processing status
# - Assignment decisions and reasoning
# - Error handling and retries
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**API Rate Limits**:
- The agent implements exponential backoff for rate limiting
- Adjust `MAX_CONCURRENT_REQUESTS` in configuration

**Authentication Errors**:
- Verify your GitHub token has proper permissions
- Ensure OpenAI API key is valid and has sufficient credits

**Assignment Logic**:
- Review assignment rules in `config/assignment_rules.yaml`
- Check logs for assignment reasoning and decisions

## 📚 Examples

See the `examples/` directory for:
- Basic usage examples
- Custom assignment rule configuration
- Integration with CI/CD pipelines
- Webhook setup for real-time processing

## 🔮 Roadmap

- [ ] Support for multiple repositories
- [ ] Web dashboard for monitoring and configuration
- [ ] Integration with Slack/Teams notifications  
- [ ] Advanced ML models for owner prediction
- [ ] Custom prompt templates for different issue types
