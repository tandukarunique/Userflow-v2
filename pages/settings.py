from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.inbox import InboxPage
import time
import random
import string

SETTING_PAGE = "//*[local-name()='svg' and .//*[local-name()='path' and contains(@d, 'M8.55345 5.3686L6.76075')]]"
COUNTRY_SELECT_SVG = "//*[local-name()='svg' and .//*[local-name()='path' and contains(@d, 'M6 9L12 15L18 9')]]"


class SETTING(InboxPage,BasePage):
    
    def go_to_setting(self):
        self.click(SETTING_PAGE)
        self.wait('medium')
        
    def account_information(self):
        random_name = ''.join(random.choices(string.ascii_letters, k=10))
        self.page.locator("#fullName").fill(random_name)
        
        phone_field = self.page.locator('#phoneNumber')
        phone_field.click()
        self.page.keyboard.press("Control+A")
        self.page.keyboard.press("Backspace")
        
        phone = f"980{random.randint(1000000, 9999999)}"
        phone_field.fill(phone)  
        
        self.page.locator(COUNTRY_SELECT_SVG).click()
        self.wait('short')
        
        self.page.get_by_role("option", name="Nepal").click()
        self.page.locator("button:has-text('Update')").click()
        print("Account information updated successfully....")
        
    def security(self):
        try:
            self.page.locator('a[href*="security"]').click()
            self.wait('short')
            self.page.locator("button:has-text('Change Password')").click()
            self.wait('short')
            self.page.locator("#old_password").fill("Tha cha 098!")
            self.page.locator("#new_password").fill("Thacha098!")
            self.page.locator("#confirm_password").fill("Thacha098!")
            self.page.get_by_role("checkbox").check()
            self.page.locator("button:has-text('Update Password')").click()
            self.wait('medium')
            print("Changed password successfully.....")
        except Exception as e:
            print(f"Error changing password: {e}")
    
    def organization_information(self):
        self.page.locator("button:has-text('Organization Settings')").click()
        self.wait('short')
        self.page.locator('a:has-text("Organization Information")').click()
        
        self.page.locator("#name").fill(f"Org_{random.randint(1000, 9999)}")
        self.page.locator("#domain").fill("demo.abc.com")
        self.page.locator("#description").fill("This is description.....")
        self.page.locator("button:has-text('Update')").click()
        
    
    #=============================================
    #Guerilla mail................................
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
         
    def team_management(self):
        self.page.get_by_text("Team Management", exact=True).click()
        self.wait('medium')
        self.page.locator("button:has-text('Invite')").first.click()

    def invite_team_member(self, email):
        self.page.locator("#email").fill(email)
        self.page.locator("#role").click()
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")
        self.page.locator("button:has-text('Invite')").last.click()
        print(f"Invite sent to {email}")

    def open_invite_link_from_mail(self, timeout=180000):
        page = getattr(self, "mail_page", self.page)
        page.bring_to_front()
        deadline = time.time() + (timeout / 1000)
        invite_row = page.locator("#email_list tr, #inbox tr").filter(
            has_not_text="no-reply@guerrillamail.com"
        ).filter(has_not_text="Welcome to Guerrilla Mail").first

        while time.time() < deadline:
            page.locator("#tick").wait_for(state="visible", timeout=10000)
            if invite_row.count() > 0 and invite_row.is_visible():
                invite_row.click()
                break
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
        else:
            raise TimeoutError("Invite email did not arrive in Guerrilla Mail.")

        page.locator("#display_email").wait_for(state="visible", timeout=30000)
        links = page.locator("#display_email a[href]").evaluate_all(
            "elements => elements.map(element => element.href)"
        )
        href = next((link for link in links if "chatboq" in link), None)
        if not href:
            raise RuntimeError(f"Invite link not found in email. Links found: {links}")

        opened_page = self.page.context.new_page()
        opened_page.goto(href, wait_until="domcontentloaded")

        opened_page.wait_for_load_state("domcontentloaded")
        print(f"Opened invite link: {href or opened_page.url}")
        return opened_page
        
    #_____________________Quick replies___________________________
    #def go_to_quickresponse(self):
    #    self.page.locator('a:has-text("Quick Replies")').click()
    #    
    #    self.page.locator("#title").click()
    #    self.page.locator("#category_id").click()
    #    self.page.locator("#shortcut").click()
    #    self.page.locator("#content").fill("This is quick reply.........")
     

    def response(self):
            self.page.locator('a:has-text("Quick Replies")').click()
            
            
            self.page.locator("button:has-text('Add Quick Reply')").click()
            self.wait('medium')  
            random_title = "Title " + ''.join(random.choices(string.ascii_letters, k=6))
            self.page.locator("#title").fill(random_title)
            self.page.locator("span:has-text('Select group')").click()
            self.page.get_by_role("option", name="ggggg").click()

            shortcut = "demo" + ''.join(random.choices(string.ascii_lowercase, k=6))
            self.page.locator("#shortcut").fill(shortcut)
            
            description = "Description"+ ''.join(random.choices(string.ascii_letters, k=6))
            self.page.locator("#content").fill(description)
            
            
            
    
        
    def create(self):
            self.page.locator("button:has-text('Create Quick Reply')").click()
        
    def private_quick_replies(self):
        self.response()
       
        self.page.get_by_role("switch").first.click()
        self.create()
        
        
