# E2E Tests Setup

## Environment Configuration

This directory uses environment-specific configuration files to manage credentials securely. Environment variables are automatically loaded once per test session and are available to all tests and fixtures.

### Setup Instructions

1. **Copy the template for each environment you need:**
   ```bash
   # Development environment
   cp env.template env.dev
   
   # QA environment  
   cp env.template env.qa
   
   # Acceptance environment
   cp env.template env.acc
   ```

2. **Edit each environment file with actual credentials:**
   ```bash
   # Edit development credentials
   nano env.dev
   
   # Edit QA credentials
   nano env.qa
   
   # Edit acceptance credentials
   nano env.acc
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

### Running Tests

The `--env` parameter is available globally and can be used from any directory:

#### All Tests (Including E2E)

```bash
# Run all tests with E2E environment
pytest --env=dev

# Run all tests with different environments
pytest --env=qa
pytest --env=acc

# Run all tests without E2E (E2E tests will be skipped)
pytest
```

#### E2E Tests Only

```bash
# Run only E2E tests with environment
pytest tests/e2e/ --env=dev

# Run only E2E tests (will be skipped without --env)
pytest tests/e2e/
```

#### Mixed Test Runs

```bash
# Run specific test types with E2E
pytest tests/e2e/ tests/functional/ --env=dev

# Run specific tests with environment
pytest tests/e2e/test_auth_with_env.py --env=qa
```

**Note:** 
- The `--env` parameter is now available globally from any directory
- If no `--env` parameter is provided, E2E tests will be **skipped** with a message indicating that environment configuration is required
- Non-E2E tests (functional, unit) are not affected by the `--env` parameter

## Using Environment Variables

### Automatic Loading

Environment variables are automatically loaded at the start of each test session using the `load_e2e_environment` fixture (autouse=True). This means:

- ✅ All tests have access to environment variables
- ✅ All fixtures can use `os.getenv()` to access configuration
- ✅ No need to manually load environment in each fixture
- ✅ Tests are skipped if no environment is specified
- ✅ Safe to run from any directory without errors
- ✅ Global `--env` option available everywhere

### Available Fixtures

#### `auth_config` - Authentication Configuration
```python
def test_example(auth_config):
    client_id = auth_config["client_id"]
    secret_id = auth_config["secret_id"]
```

### Creating Custom Fixtures

You can create fixtures that use environment variables:

```python
import os
import pytest

@pytest.fixture
def api_client():
    """Custom fixture using environment variables"""
    client_id = os.getenv("E2E_CLIENT_ID")
    secret_id = os.getenv("E2E_SECRET_ID")
    
    # Create your API client here
    return APIClient(client_id=client_id, secret_id=secret_id)
```

### Direct Access in Tests

You can also access environment variables directly in tests:

```python
import os

def test_direct_access():
    client_id = os.getenv("E2E_CLIENT_ID")
    secret_id = os.getenv("E2E_SECRET_ID")
    # Use variables directly
```

### Security Notes

- ✅ `env.template` is tracked in version control
- ❌ `env.*` files (actual credentials) are ignored by git
- 🔒 Never commit real credentials to the repository
- 📋 Use the template as a reference for required variables

### Environment Variables

Each environment file should contain:

| Variable | Description | Required |
|----------|-------------|----------|
| `E2E_CLIENT_ID` | Client ID for authentication | ✅ Yes |
| `E2E_SECRET_ID` | Secret ID for authentication | ✅ Yes |

### Adding New Environment Variables

1. Add the variable to `env.template`
2. Update your environment files (`env.dev`, `env.qa`, etc.)
3. Use `os.getenv("YOUR_VARIABLE")` in fixtures or tests
4. Optionally add it to custom fixtures in `conftest.py` 