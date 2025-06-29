"""
Basic usage examples for GitHub Issues AI Agent.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Add the parent directory to the path so we can import github_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from github_agent import GitHubIssueAgent


async def example_single_issue():
    """Example: Process a single issue."""
    load_dotenv()
    
    agent = GitHubIssueAgent()
    
    print("🎯 Processing single issue...")
    
    # Process issue #1 (replace with actual issue number)
    result = await agent.process_issue(1)
    
    if result["success"]:
        print(f"✅ Issue #{result['issue_number']} processed successfully")
        print(f"📝 Summary: {result['summary'].summary}")
        print(f"🏷️ Category: {result['summary'].category}")
        print(f"⚡ Priority: {result['summary'].priority}")
        
        if result['assignment'].assigned_owner:
            print(f"👤 Assigned to: {result['assignment'].assigned_owner}")
            print(f"🎯 Confidence: {result['assignment'].confidence_score:.2f}")
            print(f"💭 Reasoning: {result['assignment'].reasoning}")
    else:
        print(f"❌ Failed: {result['error']}")


async def example_multiple_issues():
    """Example: Process multiple specific issues."""
    load_dotenv()
    
    agent = GitHubIssueAgent()
    
    print("🎯 Processing multiple issues...")
    
    # Process issues #1, #2, #3 (replace with actual issue numbers)
    issue_numbers = [1, 2, 3]
    results = await agent.process_multiple_issues(issue_numbers)
    
    print(f"📊 Processed {len(results)} issues:")
    
    for issue_num, result in results.items():
        if result["success"]:
            print(f"  ✅ Issue #{issue_num}: {result['summary'].category}")
        else:
            print(f"  ❌ Issue #{issue_num}: {result['error']}")


async def example_all_open_issues():
    """Example: Process all open issues."""
    load_dotenv()
    
    agent = GitHubIssueAgent()
    
    print("🎯 Processing all open issues...")
    
    results = await agent.process_all_open_issues()
    
    if not results:
        print("📭 No open issues found")
        return
    
    successful = sum(1 for r in results.values() if r.get("success", False))
    total = len(results)
    
    print(f"📊 Results: {successful}/{total} issues processed successfully")
    
    # Show assignments made
    assignments = [
        r['assignment'] for r in results.values() 
        if r.get("success") and r.get('assignment', {}).get('assigned_owner')
    ]
    
    print(f"👥 Assignments made: {len(assignments)}")
    for assignment in assignments[:3]:  # Show first 3
        print(f"  • Issue #{assignment.issue_number} → {assignment.assigned_owner}")


async def example_summarization_only():
    """Example: Generate summary without assignment."""
    load_dotenv()
    
    agent = GitHubIssueAgent()
    
    print("📝 Generating AI summary...")
    
    # Summarize issue #1 (replace with actual issue number)
    summary = await agent.summarize_issue(1)
    
    print(f"Summary: {summary}")


async def example_assignment_only():
    """Example: Assign owner without full processing."""
    load_dotenv()
    
    agent = GitHubIssueAgent()
    
    print("👤 Assigning owner...")
    
    # Assign owner to issue #1 (replace with actual issue number)
    assigned_owner = await agent.assign_owner(1)
    
    if assigned_owner:
        print(f"✅ Assigned to: {assigned_owner}")
    else:
        print("❌ No suitable owner found")


async def example_health_check():
    """Example: Check system health."""
    load_dotenv()
    
    agent = GitHubIssueAgent()
    
    print("🏥 Checking system health...")
    
    health_status = await agent.health_check()
    
    for component, status in health_status.items():
        if component == 'timestamp':
            continue
        print(f"  {component}: {status}")


if __name__ == "__main__":
    print("🚀 GitHub Issues AI Agent - Examples")
    print("=" * 40)
    
    # Run different examples
    print("\n1. Single Issue Processing:")
    asyncio.run(example_single_issue())
    
    print("\n2. Health Check:")
    asyncio.run(example_health_check())
    
    # Uncomment to run other examples:
    # print("\n3. Multiple Issues:")
    # asyncio.run(example_multiple_issues())
    
    # print("\n4. All Open Issues:")
    # asyncio.run(example_all_open_issues())
