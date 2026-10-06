import pytest

from framework.polling import wait_for_booking


@pytest.mark.smoke
def test_create_booking_is_saved(client, token, booking_data):
    # data for 1 passenger
    payload = booking_data["valid"][0]

    # POST the booking
    created = client.create_booking(payload)
    assert created.status_code == 200, f"unexpected status: {created.status_code}"
    body = created.json()
    booking_id = body["bookingid"]

    try:
        assert body["booking"] == payload

        # poll GET until the booking is available, then check it was saved as sent
        fetched = wait_for_booking(client, booking_id)
        assert fetched.status_code == 200, f"booking {booking_id} not found: {fetched.status_code}"
        assert fetched.json() == payload
    finally:
        # auth is only needed to clean up - creating a booking is public
        client.delete_booking(booking_id, token=token)
