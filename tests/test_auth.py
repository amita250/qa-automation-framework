import pytest

@pytest.mark.smoke
def test_valid_credentials_return_token(client):
    token = client.get_token()
    assert token
    assert isinstance(token, str)

@pytest.mark.smoke
def test_delete_requires_authentication(client, token):
    payload = {
        "firstname": "QA",
        "lastname": "Test",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2027-01-01", "checkout": "2027-01-05"},
    }
    created = client.create_booking(payload)
    assert created.status_code == 200
    booking_id = created.json()["bookingid"]

    try:
        res = client.delete_booking(booking_id, token="invalid-token")
        assert res.status_code == 403
    finally:
        client.delete_booking(booking_id, token=token)
