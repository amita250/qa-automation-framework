import json
from pathlib import Path

import pytest

from framework.client import BookingClient

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def client():
    api = BookingClient()
    yield api
    api.close()


@pytest.fixture(scope="session")
def token(client):
    return client.get_token()


@pytest.fixture
def booking_data():
    return json.loads((DATA_DIR / "booking_data.json").read_text())