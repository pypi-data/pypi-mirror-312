import pytest
from qiscus_python_sdk.api_client import APIClient


@pytest.fixture
def sdk():
    """Fixture to initialize QiscusSDK."""
    return APIClient()


def test_login(sdk):
    response = sdk.login("rahmad@qiscus.net", "Qiscus1234!@#$")
    assert response.status_code == 200
