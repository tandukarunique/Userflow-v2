from playwright.sync_api import Page
from pages.base_page import BasePage
import time
import random
import string

SETTING_PAGE = "//*[local-name()='svg' and .//*[local-name()='path' and contains(@d, 'M8.55345 5.3686L6.76075')]]"
COUNTRY_SELECT_SVG = "//*[local-name()='svg' and .//*[local-name()='path' and contains(@d, 'M6 9L12 15L18 9')]]"


class SETTING(BasePage):
    
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
        new_page.goto("https://www.guerrillamail.com/")
        return new_page, incognito

        
    def guerilla_mail_action(self):
        self.page.locator("#use-alias").click()
        box = self.page.locator("#aippxjzc")
        box.keyboard.press("Control+A")
        box.keyboard.press("Backspace")
        box.fill("demo")
        self.page.locator("button:has-text('Set')").click()
        
        
        
        
    
    def team_management(self):
        self.page.locator('a:has-text("Team Management")').click()
        self.page.locator("button:has=text('Invite')")
        
        
        
    
    
        
    
            
        
        
        