"""
Test runner for GitHub Issues AI Agent.
"""

import pytest
import sys
from pathlib import Path

def run_tests():
    """Run all tests."""
    # Add src to path for imports
    src_path = Path(__file__).parent / "github_agent"
    sys.path.insert(0, str(src_path))
    
    # Run pytest
    pytest_args = [
        "tests/",
        "-v",
        "--tb=short",
        "--no-header"
    ]
    
    return pytest.main(pytest_args)

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
