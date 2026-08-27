from playwright.sync_api import sync_playwright
import random
import string

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=True for CI/CD
    page = browser.new_page()
    
    # Navigate to login page
    page.goto("https://www.guerrillamail.com/")
    
    # Wait for page to load
    page.wait_for_load_state("networkidle")
    
    #Change email
    def go_to_mail(self):
        incognito = self.page.context.browser.new_context()
        new_page = incognito.new_page()
        new_page.goto("https://www.guerrillamail.com/", wait_until="domcontentloaded")
        self.mail_page = new_page
        self.mail_context = incognito
        return new_page, incognito

    def guerilla_mail_action(self):
        page = getattr(self, "mail_page", self.page)
        page.locator("#use-alias").uncheck()
        page.locator("#gm-host-select").select_option("sharklasers.com")
        page.locator("#inbox-id").click()
        box = page.locator("#inbox-id input[type='text']")
        random_text = ''.join(random.choices(string.ascii_lowercase, k=8))
        box.fill(random_text)
        page.locator("button:has-text('Set')").click()
        page.locator("#inbox-id").wait_for(state="visible")
        email = f"{page.locator('#inbox-id').inner_text()}@{page.locator('#gm-host-select').input_value()}"
        print(f"Guerrilla Mail set to {email}")
        return email
    
    
    
    
    
    
    
    
    
    
    
    browser.close()