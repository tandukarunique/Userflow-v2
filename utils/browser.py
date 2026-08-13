from playwright.sync_api import Browser, BrowserContext, Playwright

from utils.auth import add_session_to_context, state_file, verify_session
from utils.config import Config


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


def launch_browser(playwright: Playwright) -> Browser:
    return playwright.chromium.launch(
        headless=Config.HEADLESS,
        slow_mo=Config.SLOW_MO,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ],
    )


def create_context(browser: Browser, session_id: str) -> BrowserContext:
    saved_state = state_file(session_id)
    options = {"user_agent": USER_AGENT, "viewport": None}
    if saved_state.exists():
        options["storage_state"] = str(saved_state)
        print(f"🔐 Reusing saved browser session: {saved_state.name}")
    else:
        print("🔐 No local browser state found; trying the supplied session UUID.")

    context = browser.new_context(**options)
    add_session_to_context(context, session_id)
    verify_session(context)
    context.add_init_script(
        """
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                { name: 'Chrome PDF Plugin' },
                { name: 'Chrome PDF Viewer' },
                { name: 'Native Client' }
            ]
        });
        """
    )
    return context
