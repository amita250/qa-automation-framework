import time

import requests

from framework.client import BookingClient


def wait_for_booking(
    client: BookingClient, booking_id: int, timeout: float = 10, interval: float = 0.5
) -> requests.Response:
    """GET the booking until it returns 200 or `timeout` seconds pass.

    Returns the last response, so the test decides what to assert.
    """
    deadline = time.monotonic() + timeout
    while True:
        response = client.get_booking(booking_id)
        if response.status_code == 200:
            return response
        if time.monotonic() >= deadline:
            return response
        time.sleep(interval)