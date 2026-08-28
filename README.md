# Userflow V2 Automation

End-to-end automation suite for validating key workflows in the Chatboq staging application. The project uses Playwright with Pytest and follows a page-object structure to keep test logic readable and reusable.

## Overview

This repository automates browser-based user flows for:

- Authentication through a reusable session UUID
- Inbox message validation and conversation actions
- Lead and CRM workflows
- Ticket creation workflows
- Settings, account, organization, team, mail, and quick-response flows

The main automation entry point is `main.py`. Test-specific coverage is available under the `tests/` directory.

## Tech Stack

- Python 3.12+
- Playwright
- Pytest
- pytest-playwright

## Project Structure

```text
.
├── main.py                 # Full automation flow runner
├── pages/                  # Page object classes and page-level actions
│   ├── base_page.py
│   ├── inbox.py
│   ├── Leadandcrm.py
│   ├── tickets.py
│   ├── settings.py
│   └── auth.py
├── tests/                  # Pytest test suites
│   ├── conftest.py
│   ├── test_inbox.py
│   ├── test_lead.py
│   └── test_lead_validation.py
├── utils/                  # Shared helpers and configuration
│   ├── auth.py
│   ├── browser.py
│   ├── config.py
│   └── mail.py
├── auth/                   # Local auth state, ignored by git
└── requirements.txt
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
python -m playwright install
```

## Authentication

The suite uses a Chatboq session UUID for authenticated test runs. The local `auth/` directory is intentionally ignored by git because it can contain session data.

Set the session ID in one of these ways:

```bash
export CHATBOQ_SESSION_ID="your-session-uuid"
```

Or create:

```text
auth/session_id.txt
```

with only the session UUID inside.

When a valid session is used, the automation saves browser storage state in `auth/<session-id>.json` for reuse.

## Configuration

Common configuration values are defined in `utils/config.py`, including:

- `BASE_URL`
- `AUTH_ME_URL`
- `AUTH_COOKIE_NAME`
- default timeouts
- browser headless mode
- browser slow motion

Headless mode can be controlled with:

```bash
CHATBOQ_HEADLESS=true pytest -s tests/test_inbox.py
```

Slow motion can be adjusted with:

```bash
CHATBOQ_SLOW_MO=100 pytest -s tests/test_inbox.py
```

## Running Automation

Run the complete scripted flow:

```bash
python main.py
```

Run all tests:

```bash
pytest -s tests
```

Run inbox tests:

```bash
pytest -s tests/test_inbox.py
```

Run lead tests:

```bash
pytest -s tests/test_lead.py
pytest -s tests/test_lead_validation.py
```


## Development Guidelines

- Keep browser interaction logic inside page objects in `pages/`.
- Keep shared browser, authentication, and configuration logic inside `utils/`.
- Add new tests under `tests/` with clear names and focused assertions.
- Avoid committing real session IDs, saved storage states, passwords, or local-only files.


