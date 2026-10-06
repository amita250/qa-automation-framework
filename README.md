# qa-automation-framework

API test-automation framework built with Python and pytest. It tests the public
[restful-booker](https://restful-booker.herokuapp.com) demo API.

> **Note:** Tests run against the live remote service, so you need network access.
> The free instance can take a while to wake up on the first request. The HTTP
> client retries on 502/503/504 responses to handle this.

## Requirements

- Python 3.11+

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
```

## Running tests

```bash
pytest                        # run everything
pytest -m smoke               # critical-path subset
pytest -m regression          # full suite
pytest tests/test_auth.py     # a single file
pytest tests/test_auth.py::test_valid_credentials_return_token   # a single test
pytest -v                     # show each test name
```

## Configuration

Settings are read from environment variables with the `QA_` prefix. You can also
put them in a `.env` file in the project root (it is git-ignored). Real environment
variables override values in `.env`.

| Variable      | Default                                | Description                |
| ------------- | -------------------------------------- | -------------------------- |
| `QA_BASE_URL` | `https://restful-booker.herokuapp.com` | API base URL               |
| `QA_USERNAME` | `admin`                                | Username for `POST /auth`  |
| `QA_PASSWORD` | `password123`                          | Password for `POST /auth`  |
| `QA_TIMEOUT`  | `15`                                   | Request timeout in seconds |

Example:

```bash
QA_BASE_URL=http://localhost:3001 QA_TIMEOUT=30 pytest
```

## Project structure

```
framework/
  config.py     # Settings (pydantic-settings, QA_ env prefix)
  client.py     # BookingClient: requests.Session + retry policy, one method per endpoint
tests/
  conftest.py   # session-scoped `client` and `token` fixtures
  test_health.py
  test_auth.py
pyproject.toml  # dependencies + pytest config (markers, strict mode)
```

### Design

- **`BookingClient` is a thin layer over the API.** Its methods return the raw
  `requests.Response` and don't make assertions. The exception is `get_token()`,
  which returns the token string and raises an error if authentication fails.
- **Tests make all the assertions**, usually on `status_code` and `json()`.
- **Fixtures are session-scoped.** The whole run shares one HTTP session and one
  auth token.

## Writing tests

- Use the `client` fixture for API calls and the `token` fixture when an endpoint
  needs authentication.
- Tag each test with a registered marker (`@pytest.mark.smoke` or
  `@pytest.mark.regression`). Because `--strict-markers` is on, any new marker must
  be added to `[tool.pytest.ini_options] markers` in `pyproject.toml` first.
- Delete any bookings your test creates. The server is shared and public, so data
  stays there otherwise.

## License

[MIT](LICENSE)