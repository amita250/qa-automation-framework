# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

API test-automation framework (Python + pytest) exercising the public `restful-booker`
demo API (https://restful-booker.herokuapp.com). Tests run against the live remote
service — network access is required, and the free instance cold-starts slowly (hence
the retry policy in the client).

## Commands

```bash
pip install -e .              # install the `framework` package (editable) + deps
pytest                        # run everything (config lives in pyproject.toml)
pytest -m smoke               # critical-path subset
pytest -m regression          # full suite
pytest tests/test_auth.py     # one file
pytest tests/test_auth.py::test_valid_credentials_return_token   # one test
pytest -v                     # show per-test names
```

There is no separate build or lint step.

## Configuration

`framework/config.py` defines a pydantic-settings `Settings` model with the `QA_` env
prefix, loaded from `.env` (real environment variables take precedence). A module-level
`settings` singleton is imported throughout. Override per-run, e.g.
`QA_BASE_URL=http://localhost:3001 pytest` or `QA_TIMEOUT=30 pytest`.

## Architecture

Three layers, each in its own place:

1. **`Settings` (`framework/config.py`)** — all configuration (`base_url`, `username`,
   `password`, `timeout`).
2. **`BookingClient` (`framework/client.py`)** — wraps a single `requests.Session` with a
   retry policy (3 retries, 0.5 backoff, on 502/503/504). One method per API operation
   (`ping`, `get_token`, `get_booking`, `create_booking`, `delete_booking`). The client is
   intentionally thin: methods return the raw `requests.Response` and make **no
   assertions**. The sole exception is `get_token()`, which returns a `str` and raises
   (`raise_for_status()` / `RuntimeError`) on failure.
3. **Tests (`tests/`)** — consume the session-scoped `client` and `token` fixtures from
   `tests/conftest.py` and own every assertion, usually on `response.status_code` and
   `response.json()`.

### Target-API behaviors the tests depend on

- `GET /ping` returns **201** (not 200) when healthy — see `test_health.py`.
- `POST /auth` always returns **200**. A bad login yields `200` with body
  `{"reason": "Bad credentials"}` and no token.
- Protected calls authenticate with a `Cookie: token=<token>` header; a missing or invalid
  token gives **403** — see `test_delete_requires_authentication`.

## Conventions & gotchas

- `pyproject.toml` sets `--strict-markers`: every `@pytest.mark.<name>` must first be
  registered under `[tool.pytest.ini_options] markers`. Only `smoke` and `regression`
  exist today.
- `get_token()` raises on failure, so it cannot drive a negative-auth test. Hit
  `client.session.post(f"{client.base}/auth", json=...)` directly, or add a helper that
  returns the raw response.
- The `client` fixture is `scope="session"` — one HTTP session for the whole run.
  `create_booking` writes to a shared public server, so created data persists there.
