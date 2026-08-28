import os
from pathlib import Path

from playwright.sync_api import BrowserContext, Page

from utils.config import Config


AUTH_DIR = Path(__file__).resolve().parent.parent / "auth"


def get_session_id() -> str:
    session_id = os.getenv("CHATBOQ_SESSION_ID", "").strip()
    if session_id:
        return session_id

    session_file = AUTH_DIR / "session_id.txt"
    if session_file.exists():
        session_id = session_file.read_text(encoding="utf-8").strip()
        if session_id:
            return session_id

    return Config.AUTH_SESSION_ID


def state_file(session_id: str) -> Path:
    return AUTH_DIR / f"{session_id}.json"


def add_session_to_context(context: BrowserContext, session_id: str) -> None:
    context.add_cookies(
        [
            {
                "name": Config.AUTH_COOKIE_NAME,
                "value": session_id,
                "domain": ".chatboq.com",
                "path": "/",
                "httpOnly": False,
                "secure": False,
                "sameSite": "Lax",
            }
        ]
    )


def verify_session(context: BrowserContext) -> bool:
    response = context.request.get(Config.AUTH_ME_URL)
    if response.ok:
        return True

    print(f"Auth check failed: {response.status} {response.status_text}")
    return False


def authenticate(
    context: BrowserContext,
    session_id: str,
    allow_manual_login: bool = True,
) -> Page:
    page = context.new_page()
    page.goto(Config.BASE_URL)
    page.evaluate(
        """sessionId => {
            window.localStorage.setItem("session_uuid", sessionId);
        }""",
        session_id,
    )
    page.reload(wait_until="domcontentloaded", timeout=Config.DEFAULT_TIMEOUT)

    if verify_session(context):
        context.storage_state(path=str(state_file(session_id)))
        return page

    if not allow_manual_login:
        page.close()
        raise RuntimeError(
            "Authentication failed. Update CHATBOQ_SESSION_ID or auth/session_id.txt."
        )

    print("Authentication failed. Log in manually in the opened browser window.")
    page.goto(f"{Config.BASE_URL.rstrip('/')}/auth/login")
    page.wait_for_timeout(Config.LONG_TIMEOUT)
    context.storage_state(path=str(state_file(session_id)))
    return page
