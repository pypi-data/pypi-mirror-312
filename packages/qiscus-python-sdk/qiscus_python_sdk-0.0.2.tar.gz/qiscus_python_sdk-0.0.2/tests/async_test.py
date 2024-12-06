import pytest
import pytest_asyncio
from qiscus_python_sdk.api_client import AsyncAPIClient


@pytest.fixture
def sdk():
    """Fixture to initialize QiscusSDK."""
    return AsyncAPIClient()


@pytest.mark.asyncio
async def test_login(sdk):
    response = await sdk.login("rahmad@qiscus.net", "Qiscus1234!@#$")
    assert response.status_code == 200
