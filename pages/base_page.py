from playwright.sync_api import Page
import random
import string

class BasePage:
    def __init__(self, page):
        self.page = page
    
    def navigate_to(self, url):
        self.page.goto(url)
        return self
    
    def wait_for_load(self):
        self.page.wait_for_load_state("load")
        return self
    
    def wait_for_element(self, selector, timeout=30000):
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        return self
    
    def click(self, selector):
        self.page.click(selector)
        return self
    
    def fill(self, selector, text):
        self.page.fill(selector, text)
        return self
    
    def is_visible(self, selector):
        try:
            return self.page.is_visible(selector)
        except:
            return False
    
    def get_text(self, selector):
        try:
            return self.page.text_content(selector)
        except:
            return None
    
    def get_current_url(self):
        return self.page.url
    
    def get_title(self):
        return self.page.title()
    
    def take_screenshot(self, name="screenshot.png"):
        self.page.screenshot(path=name)
        return self
    
    def wait_for_timeout(self, milliseconds):
        self.page.wait_for_timeout(milliseconds)
        return self
    
    def generate_random_text(self,length=5):
    
         return ''.join(random.choices(string.ascii_lowercase, k=length))