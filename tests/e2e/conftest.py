import os
from pathlib import Path

import pytest


def load_env_file(env_name):
    """Load environment variables from env file"""
    try:
        from dotenv import load_dotenv
    except ImportError:
        raise ImportError("python-dotenv is required. Install it with: pip install python-dotenv") from None

    # Get the directory where this conftest.py is located
    current_dir = Path(__file__).parent
    env_file = current_dir / f"env.{env_name}"

    if not env_file.exists():
        raise FileNotFoundError(f"Environment file not found: {env_file}")

    # Load environment variables from the specific env file
    load_dotenv(env_file)


@pytest.fixture(scope="session", autouse=True)
def load_e2e_environment(request):
    """
    Automatically load environment variables for all E2E tests.
    This fixture runs once per test session and makes environment
    variables available to all tests and fixtures.
    """
    # Get the --env option (now always available globally)
    env = request.config.getoption("--env")

    if env:
        # Load the appropriate environment file
        load_env_file(env)
        print(f"\n🔧 Loaded E2E environment: {env}")
    else:
        pytest.skip("No --env specified. E2E tests require environment configuration.")


@pytest.fixture(scope="session")
def auth_config():
    """
    Get authentication configuration from environment variables.
    Depends on load_e2e_environment fixture to ensure env vars are loaded.
    """
    # Read credentials from environment variables (already loaded by load_e2e_environment)
    client_id = os.getenv("E2E_CLIENT_ID")
    secret_id = os.getenv("E2E_SECRET_ID")

    if not client_id or not secret_id:
        raise ValueError("Missing E2E credentials. Ensure environment file is loaded with --env parameter.")

    return {"client_id": client_id, "secret_id": secret_id}
