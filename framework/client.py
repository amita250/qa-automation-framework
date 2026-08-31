import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from framework.config import settings


class BookingClient:
    def __init__(self) -> None:
        self.base = settings.base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def ping(self) -> requests.Response:
        return self.session.get(f"{self.base}/ping", timeout=settings.timeout)

    def close(self) -> None:
        self.session.close()

    def get_token(self) -> str:
        res = self.session.post(
            f"{self.base}/auth",
            json={"username": settings.username, "password": settings.password},
            timeout=settings.timeout,
        )
        res.raise_for_status()
        body = res.json()
        if "token" not in body:
            raise RuntimeError(f"auth failed: {body}")
        return body["token"]

    def get_booking(self, booking_id: int):
        return self.session.get(
            f"{self.base}/booking/{booking_id}", timeout=settings.timeout
        )

    def create_booking(self, payload: dict) -> requests.Response:
        return self.session.post(
            f"{self.base}/booking", json=payload, timeout=settings.timeout
        )

    def delete_booking(self, booking_id: int, token: str) -> requests.Response:
        return self.session.delete(
            f"{self.base}/booking/{booking_id}",
            headers={"Cookie": f"token={token}"},
            timeout=settings.timeout,
        )