import logging
import os
from datetime import datetime
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


# Fixture to automatically inject record_property for parametrized tests
@pytest.fixture(autouse=True)
def auto_record_parameters(request, record_property, caplog):
    """
    Automatically record all parametrized test parameters as properties.
    This fixture runs for every test and automatically logs parametrized data for e2e tests.
    """
    # Check if this is an e2e test
    is_e2e_test = False
    if hasattr(request.node, "iter_markers"):
        for marker in request.node.iter_markers():
            if marker.name == "e2e":
                is_e2e_test = True
                break

    # Only inject for e2e tests
    if is_e2e_test:
        # Set caplog level to capture all log messages
        caplog.set_level(logging.INFO)

        # Record environment information
        env = request.config.getoption("--env", default="unknown")
        record_property("test_environment", env)

        # Record test metadata
        record_property("test_file", str(request.node.fspath))
        record_property("test_timestamp", datetime.now().isoformat())

        # Record parametrized test parameters
        if hasattr(request.node, "callspec"):
            for param_name, param_value in request.node.callspec.params.items():
                record_property(f"param_{param_name}", str(param_value))
