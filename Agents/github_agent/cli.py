"""
Command-line interface for GitHub Issues AI Agent.
"""

import asyncio
import click
from typing import List

from .agent import GitHubIssueAgent
from .config import get_settings
from .utils import format_processing_time


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """GitHub Issues AI Agent - Intelligent issue summarization and assignment."""
    pass


@cli.command()
@click.option(
    '--issue', '-i', 
    type=int, 
    help='Process a specific issue number'
)
@click.option(
    '--all', '-a', 
    is_flag=True, 
    help='Process all open issues'
)
@click.option(
    '--labels', '-l', 
    help='Filter issues by labels (comma-separated)'
)
@click.option(
    '--dry-run', '-d', 
    is_flag=True, 
    help='Perform dry run without making changes'
)
@click.option(
    '--verbose', '-v', 
    is_flag=True, 
    help='Enable verbose output'
)
def process(issue: int, all: bool, labels: str, dry_run: bool, verbose: bool):
    """Process GitHub issues for summarization and owner assignment."""
    
    if not (issue or all):
        click.echo("Error: Must specify either --issue or --all")
        return
    
    if issue and all:
        click.echo("Error: Cannot specify both --issue and --all")
        return
    
    # Set up configuration
    settings = get_settings()
    if dry_run:
        settings.enable_dry_run = True
    if verbose:
        settings.log_level = "DEBUG"
    
    # Run the processing
    asyncio.run(_run_processing(settings, issue, all, labels))


@cli.command()
@click.option(
    '--issue', '-i',
    type=int,
    required=True,
    help='Issue number to summarize'
)
def summarize(issue: int):
    """Generate AI summary for a specific issue."""
    settings = get_settings()
    asyncio.run(_run_summarization(settings, issue))


@cli.command()
@click.option(
    '--issue', '-i',
    type=int, 
    required=True,
    help='Issue number to assign owner'
)
@click.option(
    '--dry-run', '-d',
    is_flag=True,
    help='Show assignment without making changes'
)
def assign(issue: int, dry_run: bool):
    """Assign owner to a specific issue."""
    settings = get_settings()
    if dry_run:
        settings.enable_dry_run = True
    
    asyncio.run(_run_assignment(settings, issue))


@cli.command()
def health():
    """Check the health status of all components."""
    try:
        settings = get_settings()
    except Exception as e:
        click.echo(f"❌ Configuration Error: {e}")
        click.echo("\n💡 Please ensure you have:")
        click.echo("1. Created a .env file with required variables")
        click.echo("2. Set OPENAI_API_KEY, GITHUB_TOKEN, GITHUB_OWNER, "
                   "and GITHUB_REPO")
        click.echo("3. See .env.example for reference")
        return
    
    asyncio.run(_run_health_check(settings))


@cli.command()
def stats():
    """Show processing statistics."""
    settings = get_settings()
    agent = GitHubIssueAgent(settings)
    
    stats = agent.get_processing_stats()
    
    click.echo("\n📊 GitHub Issues AI Agent Statistics")
    click.echo("=" * 40)
    click.echo(f"Total Issues Processed: {stats.total_issues}")
    click.echo(f"Successful Summaries: {stats.successful_summaries}")
    click.echo(f"Successful Assignments: {stats.successful_assignments}")
    click.echo(f"Failed Operations: {stats.failed_operations}")
    
    if stats.total_issues > 0:
        success_rate = (
            (stats.successful_summaries + stats.successful_assignments) / 
            (stats.total_issues * 2) * 100
        )
        click.echo(f"Success Rate: {success_rate:.1f}%")
        
        if stats.processing_time > 0:
            click.echo(f"Total Processing Time: {format_processing_time(stats.processing_time)}")
            click.echo(f"Average Time per Issue: {format_processing_time(stats.average_processing_time)}")


async def _run_processing(settings, issue: int, all: bool, labels: str):
    """Run the main processing logic."""
    agent = GitHubIssueAgent(settings)
    
    click.echo("🚀 Starting GitHub Issues AI Agent...")
    
    # Health check first
    health_status = await agent.health_check()
    unhealthy_components = [
        comp for comp, status in health_status.items() 
        if not status.startswith('healthy')
    ]
    
    if unhealthy_components:
        click.echo(f"⚠️  Warning: Some components are unhealthy: {', '.join(unhealthy_components)}")
    
    try:
        if issue:
            # Process single issue
            click.echo(f"Processing issue #{issue}...")
            result = await agent.process_issue(issue)
            
            if result["success"]:
                click.echo(f"✅ Successfully processed issue #{issue}")
                click.echo(f"📝 Summary: {result['summary'].summary}")
                if result['assignment'].assigned_owner:
                    click.echo(f"👤 Assigned to: {result['assignment'].assigned_owner}")
                    click.echo(f"🎯 Confidence: {result['assignment'].confidence_score:.2f}")
            else:
                click.echo(f"❌ Failed to process issue #{issue}: {result['error']}")
        
        elif all:
            # Process all open issues
            click.echo("Processing all open issues...")
            results = await agent.process_all_open_issues()
            
            successful = sum(1 for r in results.values() if r.get("success", False))
            total = len(results)
            
            click.echo(f"✅ Processed {successful}/{total} issues successfully")
            
            # Show summary of assignments
            assignments = [
                r['assignment'] for r in results.values() 
                if r.get("success") and r.get('assignment', {}).get('assigned_owner')
            ]
            
            if assignments:
                click.echo(f"👥 Made {len(assignments)} assignments:")
                for assignment in assignments[:5]:  # Show first 5
                    click.echo(f"  • Issue #{assignment.issue_number} → {assignment.assigned_owner}")
                
                if len(assignments) > 5:
                    click.echo(f"  ... and {len(assignments) - 5} more")
        
        # Show final statistics
        stats = agent.get_processing_stats()
        click.echo(f"\n📊 Processing completed in {format_processing_time(stats.processing_time)}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")


async def _run_summarization(settings, issue: int):
    """Run summarization for a specific issue."""
    agent = GitHubIssueAgent(settings)
    
    try:
        click.echo(f"🤖 Generating AI summary for issue #{issue}...")
        summary = await agent.summarize_issue(issue)
        
        click.echo(f"\n📝 AI Summary:")
        click.echo("-" * 40)
        click.echo(summary)
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")


async def _run_assignment(settings, issue: int):
    """Run owner assignment for a specific issue."""
    agent = GitHubIssueAgent(settings)
    
    try:
        click.echo(f"👤 Assigning owner for issue #{issue}...")
        assigned_owner = await agent.assign_owner(issue)
        
        if assigned_owner:
            click.echo(f"✅ Assigned issue #{issue} to: {assigned_owner}")
        else:
            click.echo(f"❌ Could not determine appropriate owner for issue #{issue}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")


async def _run_health_check(settings):
    """Run health check on all components."""
    click.echo("🏥 Checking component health...")
    
    # First check basic configuration
    click.echo("\n🔧 Configuration Check:")
    click.echo("-" * 30)
    
    config_issues = []
    if (not settings.openai_api_key or
            settings.openai_api_key == "your-openai-api_key-here"):
        config_issues.append("OpenAI API key not set")
        
    if (not settings.github_token or
            settings.github_token == "your-github-token-here"):
        config_issues.append("GitHub token not set")
        
    if (not settings.github_owner or
            settings.github_owner == "your-github-username"):
        config_issues.append("GitHub owner not set")
        
    if (not settings.github_repo or
            settings.github_repo == "your-repo-name"):
        config_issues.append("GitHub repo not set")
    
    if config_issues:
        click.echo("❌ Configuration Issues Found:")
        for issue in config_issues:
            click.echo(f"   • {issue}")
        click.echo("\n💡 Please update your .env file with valid credentials")
        return
    
    click.echo("✅ Configuration looks good!")
    
    try:
        agent = GitHubIssueAgent(settings)
        health_status = await agent.health_check()
        
        click.echo("\n🎯 Health Status Report:")
        click.echo("-" * 30)
        
        for component, status in health_status.items():
            if component == 'timestamp':
                continue
                
            if status == 'healthy':
                click.echo(f"✅ {component.replace('_', ' ').title()}: Healthy")
            else:
                comp_name = component.replace('_', ' ').title()
                click.echo(f"❌ {comp_name}: {status}")
                
        click.echo(f"\n🕒 Checked at: {health_status['timestamp']}")
        
        unhealthy_components = [
            comp for comp, status in health_status.items()
            if status != 'healthy' and comp != 'timestamp'
        ]
        
        if unhealthy_components:
            unhealthy_list = ', '.join(unhealthy_components)
            click.echo(f"⚠️  Warning: Some components are unhealthy: {unhealthy_list}")
        else:
            click.echo("✅ All components are healthy!")
            
    except Exception as e:
        click.echo(f"❌ Failed to initialize agent: {e}")


if __name__ == '__main__':
    cli()
