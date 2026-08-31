import pytest


@pytest.mark.smoke
def test_api_is_alive(client):
    res = client.ping()
    assert res.status_code == 201, f"unexpected status: {res.status_code}"