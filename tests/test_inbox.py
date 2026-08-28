import pytest
from playwright.sync_api import Error, TimeoutError, expect
from playwright.sync_api import BrowserContext, Page, sync_playwright

from pages.inbox import InboxPage
from utils.auth import authenticate
from utils.browser import create_context, launch_browser


MESSAGE_TOO_LONG_WARNING = "Message is too long. Maximum 10000 characters allowed."


@pytest.fixture(scope="session", name="logged_in_context")
def logged_in_context_fixture(session_id: str):
    with sync_playwright() as playwright:
        browser = launch_browser(playwright)
        context: BrowserContext = create_context(browser, session_id)
        try:
            yield context
        finally:
            context.close()
            browser.close()


@pytest.fixture(scope="session", name="authenticated_page")
def authenticated_page_fixture(logged_in_context, session_id: str):
    page: Page = authenticate(logged_in_context, session_id, allow_manual_login=False)
    try:
        yield page
    finally:
        page.close()


@pytest.fixture(name="inbox_page")
def inbox_page_fixture(authenticated_page: Page):
    inbox = InboxPage(authenticated_page)
    inbox.go_to_inbox()
    inbox.select_convo()
    return inbox


# ==================== EMPTY/WHITESPACE EDGE CASES ====================

def test_inbox_does_not_send_empty_space(inbox_page):
    """Inbox should reject empty/whitespace-only messages."""
    message = "   "
    send_button = inbox_page.page.locator(inbox_page.SEND_BTN)

    try:
        inbox_page.type_message(message)

        expect(send_button).to_be_disabled()
        print("PASS: Inbox rejected empty-space message.")
    except AssertionError:
        print("FAIL: Inbox accepted empty-space message.")
        raise


def test_inbox_does_not_send_empty_string(inbox_page):
    """Inbox should reject completely empty messages."""
    send_button = inbox_page.page.locator(inbox_page.SEND_BTN)

    try:
        
        expect(send_button).to_be_disabled()
        print("PASS: Inbox rejected empty message.")
    except AssertionError:
        print("FAIL: Inbox accepted empty message.")
        raise


def test_inbox_does_not_send_newline_only(inbox_page):
    """Inbox should reject messages containing only newlines."""
    message = "\n\n\n"
    send_button = inbox_page.page.locator(inbox_page.SEND_BTN)

    try:
        inbox_page.type_message(message)
        expect(send_button).to_be_disabled()
        print("PASS: Inbox rejected newline-only message.")
    except AssertionError:
        print("FAIL: Inbox accepted newline-only message.")
        raise


def test_inbox_does_not_send_tabs_only(inbox_page):
    
    message = "\t\t\t"
    send_button = inbox_page.page.locator(inbox_page.SEND_BTN)

    try:
        inbox_page.type_message(message)
        expect(send_button).to_be_disabled()
        print("PASS: Inbox rejected tabs-only message.")
    except AssertionError:
        print("FAIL: Inbox accepted tabs-only message.")
        raise


# ==================== SPECIAL CHARACTERS EDGE CASES ====================

def test_inbox_sends_emoji(inbox_page):
    """Inbox should send and show an emoji message."""
    message = "✅"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent emoji message.")
    except AssertionError:
        print("FAIL: Inbox did not send emoji message.")
        raise


def test_inbox_sends_multiple_emojis(inbox_page):
    """Inbox should send a message with multiple different emojis."""
    message = "✅❌⭐🔥💀🎉😊❌⭐🔥💀🎉😊😂🤣"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent multiple emojis message.")
    except AssertionError:
        print("FAIL: Inbox did not send multiple emojis message.")
        raise


def test_inbox_sends_special_characters(inbox_page):
    """Inbox should send messages with special characters."""
    message = "!@#$%^&*()” ‘ ’ •_+{}|:<>?~`"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent special characters message.")
    except AssertionError:
        print("FAIL: Inbox did not send special characters message.")
        raise


def test_inbox_sends_unicode_characters(inbox_page):
    """Inbox should send messages with various Unicode characters."""
    message = "你好世界 こんにちは 세계  안녕 áa̴a̷a̸Z͑̓̾͂͗͛̐̎̽͆̋̇"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent Unicode characters message.")
    except AssertionError:
        print("FAIL: Inbox did not send Unicode characters message.")
        raise


def test_inbox_sends_mixed_script(inbox_page):
    """Inbox should send messages mixing different scripts."""
    message = "Hello 世界 123 ✅ !@# a̴a̴  s"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent mixed script message.")
    except AssertionError:
        print("FAIL: Inbox did not send mixed script message.")
        raise


def test_inbox_sends_html_special_chars(inbox_page):
    """Inbox should properly handle HTML special characters."""
    message = "<script>alert('xss')</script> <div>test</div> &nbsp <b>sdsdsd</b>;"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent HTML special characters message.")
    except AssertionError:
        print("FAIL: Inbox did not send HTML special characters message.")
        raise


# ==================== LENGTH EDGE CASES ====================

def test_inbox_sends_hugeinput(inbox_page):
    """Inbox should show validation for a message over 10000 characters."""
    message = "A" * 12000
    warning = inbox_page.page.get_by_text(MESSAGE_TOO_LONG_WARNING)
    
    try:
        inbox_page.type_message(message)
        inbox_page.send_message()
        
        expect(warning).to_be_visible()
        print("PASS: Inbox showed message-too-long warning for large text.")
    except (AssertionError, Error, TimeoutError):
        print("FAIL: Inbox did not show message-too-long warning for large text.")
        raise


def test_inbox_sends_laarge_emoji(inbox_page):
    """Inbox should show validation for a large emoji message."""
    message = "✅" * 10001
    warning = inbox_page.page.get_by_text(MESSAGE_TOO_LONG_WARNING)

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(warning).to_be_visible()
        print("PASS: Inbox showed message-too-long warning for large emoji message.")
    except (AssertionError, Error, TimeoutError):
        print("FAIL: Inbox did not show message-too-long warning for large emoji message.")
        raise


def test_inbox_sends_exactly_10000_chars(inbox_page):
    """Inbox should accept a message of exactly 10000 characters."""
    message = "A" * 10000

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent exactly 10000 character message.")
    except (AssertionError, Error, TimeoutError):
        print("FAIL: Inbox did not send exactly 10000 character message.")
        raise


def test_inbox_sends_9999_chars(inbox_page):
    """Inbox should accept a message of 9999 characters."""
    message = "A" * 9999

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent 9999 character message.")
    except (AssertionError, Error, TimeoutError):
        print("FAIL: Inbox did not send 9999 character message.")
        raise


def test_inbox_sends_12221_chars(inbox_page):
    """Inbox should reject a message of 10001 characters."""
    message = "A" * 10001
    warning = inbox_page.page.get_by_text(MESSAGE_TOO_LONG_WARNING)

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(warning).to_be_visible()
        print("PASS: Inbox rejected 10001 character message.")
    except (AssertionError, Error, TimeoutError):
        print("FAIL: Inbox did not reject 10001 character message.")
        raise


# ==================== LINE BREAKS AND FORMATTING ====================

def test_inbox_sends_multiline_message(inbox_page):
    """Inbox should send multi-line messages."""
    message = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent multi-line message.")
    except AssertionError:
        print("FAIL: Inbox did not send multi-line message.")
        raise


def test_inbox_sends_message_with_paragraphs(inbox_page):
    """Inbox should send messages with multiple paragraphs."""
    message = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent message with paragraphs.")
    except AssertionError:
        print("FAIL: Inbox did not send message with paragraphs.")
        raise


def test_inbox_sends_message_with_carriage_returns(inbox_page):
    """Inbox should handle different line endings."""
    message = "Line 1\r\nLine 2\r\nLine 3"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent message with carriage returns.")
    except AssertionError:
        print("FAIL: Inbox did not send message with carriage returns.")
        raise


# ==================== WHITESPACE IN MESSAGES ====================

def test_inbox_sends_message_with_leading_spaces(inbox_page):
    """Inbox should send messages with leading spaces."""
    message = "     This has leading spaces"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent message with leading spaces.")
    except AssertionError:
        print("FAIL: Inbox did not send message with leading spaces.")
        raise


def test_inbox_sends_message_with_trailing_spaces(inbox_page):
    """Inbox should send messages with trailing spaces."""
    message = "This has trailing spaces     "

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent message with trailing spaces.")
    except AssertionError:
        print("FAIL: Inbox did not send message with trailing spaces.")
        raise


def test_inbox_sends_message_with_multiple_spaces(inbox_page):
    """Inbox should handle multiple spaces between words."""
    message = "This    has    multiple    spaces"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent message with multiple spaces.")
    except AssertionError:
        print("FAIL: Inbox did not send message with multiple spaces.")
        raise


# ==================== NUMBER AND SYMBOL EDGE CASES ====================




def test_inbox_sends_large_numbers(inbox_page):
    """Inbox should send messages with large numbers."""
    message = "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent message with large numbers.")
    except AssertionError:
        print("FAIL: Inbox did not send message with large numbers.")
        raise


# ==================== URL AND LINK EDGE CASES ====================

def test_inbox_sends_url(inbox_page):
    """Inbox should send messages containing URLs."""
    message = "Check this out: https://example.com"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent message with URL.")
    except AssertionError:
        print("FAIL: Inbox did not send message with URL.")
        raise


def test_inbox_sends_multiple_urls(inbox_page):
    """Inbox should send messages containing multiple URLs."""
    message = "https://example.com and http://test.com and https://site.org"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent message with multiple URLs.")
    except AssertionError:
        print("FAIL: Inbox did not send message with multiple URLs.")
        raise



# ==================== PERFORMANCE AND STRESS EDGE CASES ====================

def test_inbox_sends_rapid_messages(inbox_page):
    """Inbox should handle rapid message sending."""
    messages = ["Message 1", "Message 2", "Message 3", "Message 4", "Message 5"]

    try:
        for i, msg in enumerate(messages):
            inbox_page.type_message(msg)
            inbox_page.send_message()
            # Small delay to prevent rate limiting
            inbox_page.page.wait_for_timeout(100)

        # Verify last message
        expect(inbox_page.page.locator(f"text={messages[-1]}").last).to_be_visible()
        print("PASS: Inbox sent rapid messages.")
    except (AssertionError, Error, TimeoutError):
        print("FAIL: Inbox failed to send rapid messages.")
        raise


def test_inbox_sends_long_running_conversation(inbox_page):
    """Inbox should handle a long conversation with many messages."""
    num_messages = 20

    try:
        for i in range(num_messages):
            message = f"Message #{i+1}: This is a test message with some content."
            inbox_page.type_message(message)
            inbox_page.send_message()
            inbox_page.page.wait_for_timeout(50)

        # Verify last message
        last_message = f"Message #{num_messages}: This is a test message with some content."
        expect(inbox_page.page.locator(f"text={last_message}").last).to_be_visible()
        print(f"PASS: Inbox sent {num_messages} messages in a row.")
    except (AssertionError, Error, TimeoutError):
        print("FAIL: Inbox failed to send long conversation.")
        raise


def test_inbox_sends_message_with_repeated_characters(inbox_page):
    """Inbox should handle messages with repeated characters."""
    message = "A" * 100 + "B" * 100 + "C" * 100

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent message with repeated characters.")
    except AssertionError:
        print("FAIL: Inbox did not send message with repeated characters.")
        raise


# ==================== MIXED CONTENT EDGE CASES ====================

def test_inbox_sends_mixed_content(inbox_page):
    """Inbox should send messages mixing different content types."""
    message = "Hello @user! Check https://example.com with ✅ and $100"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent mixed content message.")
    except AssertionError:
        print("FAIL: Inbox did not send mixed content message.")
        raise


# ==================== INJECTION ATTEMPTS ====================


def test_inbox_sends_xss_injection_attempt(inbox_page):
    """Inbox should safely handle XSS injection attempts."""
    message = "<img src=x onerror=alert('XSS')>"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        # Check that the message appears as text, not executed
        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox safely handled XSS injection attempt.")
    except AssertionError:
        print("FAIL: Inbox did not handle XSS injection attempt properly.")
        raise


# ==================== VERY SHORT MESSAGES ====================

def test_inbox_sends_one_character(inbox_page):
    """Inbox should send single character messages."""
    for char in ["a", "1", "!", "😊"]:
        try:
            inbox_page.type_message(char)
            inbox_page.send_message()

            expect(inbox_page.page.locator(f"text={char}").last).to_be_visible()
            print(f"PASS: Inbox sent single character '{char}'.")
        except AssertionError:
            print(f"FAIL: Inbox did not send single character '{char}'.")
            raise


def test_inbox_sends_two_characters(inbox_page):
    """Inbox should send two character messages."""
    message = "Hi"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent two character message.")
    except AssertionError:
        print("FAIL: Inbox did not send two character message.")
        raise


# ==================== CROSS-PLATFORM CHARACTERS ====================

def test_inbox_sends_math_symbols(inbox_page):
    """Inbox should send mathematical symbols."""
    message = "∑ ∫ ∏ √ ∞ ≈ ≠ ≤ ≥ ± × ÷"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent mathematical symbols.")
    except AssertionError:
        print("FAIL: Inbox did not send mathematical symbols.")
        raise


def test_inbox_sends_arrows(inbox_page):
    """Inbox should send arrow symbols."""
    message = "← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙"

    try:
        inbox_page.type_message(message)
        inbox_page.send_message()

        expect(inbox_page.page.locator(f"text={message}").last).to_be_visible()
        print("PASS: Inbox sent arrow symbols.")
    except AssertionError:
        print("FAIL: Inbox did not send arrow symbols.")
        raise


#pytest -s tests/test_inbox.py
