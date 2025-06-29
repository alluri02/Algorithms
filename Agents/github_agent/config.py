"""
Configuration management for GitHub Issues AI Agent.
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"
    openai_max_tokens: int = 2000
    openai_temperature: float = 0.3
    
    # GitHub Configuration
    github_token: str
    github_owner: str
    github_repo: str
    github_base_url: str = "https://api.github.com"
    
    # Agent Configuration
    log_level: str = "INFO"
    max_concurrent_requests: int = 5
    assignment_rules_file: str = "config/assignment_rules.yaml"
    enable_dry_run: bool = False
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # Optional Configuration
    webhook_secret: Optional[str] = None
    webhook_port: int = 8080
    database_url: str = "sqlite:///github_agent.db"
    cache_ttl: int = 3600


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
