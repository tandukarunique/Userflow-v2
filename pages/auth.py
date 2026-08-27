from playwright.sync_api import sync_playwright
from pages.settings import SETTING

class AuthPage:
    def __init__(self, page):
        self.page = page
        self.settings = SETTING(page)
    
    def navigate_to_login(self):
        self.page.goto("https://stagingv2.chatboq.com/auth/login")
        self.page.wait_for_load_state("networkidle")
    
    def click_sign_up(self):
        self.page.locator('a:has-text("Sign up")').click()
        self.page.wait_for_load_state("networkidle")
    
    def mail_actions(self):
        self.settings.go_to_mail()
    
    def verify_sign_up_page(self):
        assert self.page.url == "https://stagingv2.chatboq.com/auth/sign-up"
        print(f"✅ Successfully navigated to: {self.page.url}")

# Standalone function for mail actions
def mail_actions(settings_instance):
    settings_instance.go_to_mail()

# Main execution
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Create instance of AuthPage
    auth = AuthPage(page)
    
    # Navigate to login
    auth.navigate_to_login()
    
    # Click Sign up
    auth.click_sign_up()
    
    # Use standalone mail_actions function
    mail_actions(auth.settings)
    
    # Verify
    auth.verify_sign_up_page()
    
    input("Press Enter to close browser...")
    browser.close()