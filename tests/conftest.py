import os
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Page, sync_playwright

from pages.Leadandcrm import LeadAndCRMPage
from utils.auth import authenticate
from utils.browser import create_context, launch_browser


@pytest.fixture(scope="session", name="session_id")
def session_id_fixture() -> str:
    value = os.getenv("CHATBOQ_SESSION_ID")
    if value:
        return value.strip()

    session_file = Path(__file__).resolve().parent.parent / "auth" / "session_id.txt"
    if not session_file.exists():
        pytest.fail("Set CHATBOQ_SESSION_ID or create auth/session_id.txt before testing.")
    return session_file.read_text(encoding="utf-8").strip()


@pytest.fixture(scope="session", name="browser_page")
def browser_page_fixture(session_id: str):
    with sync_playwright() as playwright:
        browser = launch_browser(playwright)
        context: BrowserContext = create_context(browser, session_id)
        try:
            page: Page = authenticate(context, session_id, allow_manual_login=False)
            lead_page = LeadAndCRMPage(page)
            lead_page.go_to_lead()
            yield lead_page
        finally:
            context.close()
            browser.close()


@pytest.fixture(name="lead_form")
def lead_form_fixture(browser_page: LeadAndCRMPage):
    browser_page.open_new_lead()
    return browser_page