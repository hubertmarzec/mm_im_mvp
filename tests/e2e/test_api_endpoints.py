import logging

import pytest

# Configure logging to ensure messages are captured by pytest
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@pytest.mark.e2e
def describe_request():
    def will_auth_with_env(auth_config, record_property, caplog):
        client_id = auth_config["client_id"]
        secret_id = auth_config["secret_id"]

        record_property("client_id", client_id)
        record_property("secret_id", secret_id)

        logger.info("Additional evidence from test execution")
        # Your test logic
        assert client_id is not None
        assert secret_id is not None
        logger.info("Are important data which should be visible in the report")

        record_property("param_logs", caplog.text)

    # def will_fail():
    #     logger.info("Example of failing test")
    #     # Your test logic
    #     assert True is False
    #     assert secret_id is not None

    @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 54)])
    def will_pass_parametrized_test(test_input, expected, record_property, caplog):
        # Set caplog level to capture all log messages
        caplog.set_level(logging.INFO)

        logger.info(f"Testing calculation: {test_input} = {expected}")
        assert eval(test_input) == expected
        logger.info(f"Test passed: {test_input} = {expected}")

        record_property("param_logs", caplog.text)
