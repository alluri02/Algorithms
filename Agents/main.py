"""
Main entry point for GitHub Issues AI Agent.
"""

import asyncio
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not available.")

from github_agent import GitHubIssueAgent
from github_agent.config import get_settings


async def main():
    """Main entry point for the agent."""
    # Load environment variables
    load_dotenv()
    
    # Get settings with error handling
    try:
        settings = get_settings()
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Please ensure you have:")
        print("1. Created a .env file with required variables")
        print("2. Set OPENAI_API_KEY, GITHUB_TOKEN, GITHUB_OWNER, "
              "and GITHUB_REPO")
        print("3. See .env.example for reference")
        sys.exit(1)
    
    # Initialize agent
    agent = GitHubIssueAgent(settings)
    
    print("🚀 GitHub Issues AI Agent")
    print("=" * 40)
    
    # Perform health check
    print("Checking system health...")
    health_status = await agent.health_check()
    
    print(f"Agent Status: {health_status['agent']}")
    print(f"GitHub Connector: {health_status['github_connector']}")
    print(f"Summarizer: {health_status['summarizer']}")
    print(f"Owner Assigner: {health_status['owner_assigner']}")
    
    # Check if all components are healthy
    all_healthy = all(
        status == 'healthy'
        for key, status in health_status.items()
        if key != 'timestamp'
    )
    
    if not all_healthy:
        print("\n❌ Some components are not healthy. "
              "Please check configuration.")
        return
    
    print("\n✅ All systems operational!")
    
    # Example usage
    if len(sys.argv) > 1:
        issue_number = int(sys.argv[1])
        print(f"\n🎯 Processing issue #{issue_number}...")
        
        result = await agent.process_issue(issue_number)
        
        if result["success"]:
            print(f"✅ Successfully processed issue #{issue_number}")
            print(f"📝 Summary: {result['summary'].summary}")
            if result['assignment'].assigned_owner:
                print(f"👤 Assigned to: {result['assignment'].assigned_owner}")
        else:
            print(f"❌ Failed to process issue: {result['error']}")
    else:
        print("\n💡 Usage examples:")
        print("  python main.py 123                    # Process issue #123")
        print("  python -m github_agent.cli --help     # Show CLI help")
        print("  python -m github_agent.cli --all      # Process all issues")


if __name__ == "__main__":
    asyncio.run(main())
