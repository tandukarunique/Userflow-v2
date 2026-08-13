import argparse
import json
import os
from pathlib import Path

from playwright.sync_api import BrowserContext, Page

from utils.config import Config


AUTH_DIR = Path(__file__).resolve().parent.parent / "auth"
SESSION_ID_FILE = AUTH_DIR / "session_id.txt"


def _valid_session_id(session_id: str) -> str:
    session_id = session_id.strip()
    if not session_id or Path(session_id).name != session_id:
        raise ValueError("Session ID must be a non-empty filename-safe value.")
    return session_id


def save_session_id(session_id: str) -> None:
    session_id = _valid_session_id(session_id)
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_ID_FILE.write_text(session_id + "\n", encoding="utf-8")


def get_session_id() -> str:
    parser = argparse.ArgumentParser(description="Run Chatboq browser automation")
    parser.add_argument("--session-id", help="Use and save a different session ID")
    args = parser.parse_args()

    session_id = args.session_id or os.getenv("CHATBOQ_SESSION_ID")
    if session_id:
        save_session_id(session_id)
        print(f"💾 Session ID saved to: {SESSION_ID_FILE}")
        return _valid_session_id(session_id)

    if SESSION_ID_FILE.exists():
        session_id = SESSION_ID_FILE.read_text(encoding="utf-8")
        print(f"🔐 Using saved session ID from: {SESSION_ID_FILE}")
        return _valid_session_id(session_id)

    if os.isatty(0):
        session_id = input(f"Session ID [{Config.AUTH_SESSION_ID}]: ").strip()
        if session_id:
            save_session_id(session_id)
            print(f"💾 Session ID saved to: {SESSION_ID_FILE}")
            return session_id

    return _valid_session_id(Config.AUTH_SESSION_ID)


def state_file(session_id: str) -> Path:
    return AUTH_DIR / f"{_valid_session_id(session_id)}.json"


def add_session_to_context(context: BrowserContext, session_id: str) -> None:
    session_id = _valid_session_id(session_id)
    context.add_cookies([
        {
            "name": Config.AUTH_COOKIE_NAME,
            "value": session_id,
            "domain": ".chatboq.com",
            "path": "/",
        }
    ])
    context.add_init_script(
        f"localStorage.setItem({json.dumps(Config.AUTH_COOKIE_NAME)}, "
        f"{json.dumps(session_id)});"
    )


def verify_session(context: BrowserContext) -> None:
    response = context.request.get(Config.AUTH_ME_URL)
    if response.ok:
        print(f"✅ Session accepted by auth API ({response.status}).")
    else:
        print(f"⚠️ Auth API rejected the session ({response.status}).")


def authenticate(
    context: BrowserContext,
    session_id: str,
    allow_manual_login: bool = True,
) -> Page:
    saved_state = state_file(session_id)
    page = context.new_page()
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")

    logged_in = "/login" not in page.url.lower()
    if not logged_in and not saved_state.exists() and allow_manual_login:
        input("\nSession rejected. Complete login in the browser, then press Enter...")
        logged_in = "/login" not in page.url.lower()
        if not logged_in:
            raise RuntimeError("Browser still on login page.")

    if logged_in and not saved_state.exists():
        saved_state.parent.mkdir(parents=True, exist_ok=True)
        context.storage_state(path=str(saved_state))
        print(f"💾 Browser session saved to: {saved_state}")
    elif not logged_in:
        raise RuntimeError("Saved session expired. Use a valid session ID.")

    print("✅ Login successful!")
    return page
