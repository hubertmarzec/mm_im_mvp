import pytest


@pytest.mark.e2e
def test_auth_with_env(auth_config):
    client_id = auth_config["client_id"]
    secret_id = auth_config["secret_id"]
    print(f"??? client_id: {client_id}, secret_id: {secret_id}")
    # Your test logic
    assert client_id is not None
    assert secret_id is not None
