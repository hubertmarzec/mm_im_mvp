import pytest


@pytest.mark.e2e
def describe_e2e():
    def will_auth_with_env(auth_config):
        client_id = auth_config["client_id"]
        secret_id = auth_config["secret_id"]
        # Your test logic
        assert client_id is not None
        assert secret_id is not None

    @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 54)])
    def will_pass_parametrized_test(test_input, expected):
        assert eval(test_input) == expected
