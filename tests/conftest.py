import pytest

from framework.client import BookingClient


@pytest.fixture(scope="session")
def client():
    api = BookingClient()
    yield api
    api.close()


@pytest.fixture(scope="session")
def token(client):
    return client.get_token()