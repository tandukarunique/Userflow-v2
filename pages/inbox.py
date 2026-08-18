from playwright.sync_api import Page
from pages.base_page import BasePage
import time
import random
import string


class InboxPage(BasePage):
    
    TIMEOUTS = {
           'short': 500,
           'medium': 1000,
           'long': 2000,
           'verylong': 7000,  
       }
    
    INBOX_PAGE = "//*[local-name()='svg' and .//*[local-name()='path' and contains(@d, 'M4.75195 7.75098H15.252C16.3565')]]"
    PERSON_SVG = "//*[local-name()='svg' and .//*[local-name()='path' and contains(@d, 'M12.002 12.2422C14.4872')]]"
    MESSAGE_ACTION_SVG = "//*[local-name()='path' and contains(@d, 'M14 5C14 3.89543 13.1046 3 12 ')]/ancestor::*[local-name()='svg']"
    NOTE_ACTION_SVG = "//button[.//*[local-name()='path' and contains(@d, 'M14 5C14 3.89543 13.1046 3 12 ')]]"
    SHOW_DELETED = "//*local-name()='svg' and .//*local-name()='path' and contains(@d, 'M13 17.25C16.4518 17.25')"
    FORMATTING = "button:has(svg path[d*='M2.00797 18.6496C2.52996 18.6496 2.82695 18.3976'])"
    SEND_BTN = "button:has(svg path[d*='M9.50929 4.23111L18.0693 8.51111'])"
    BOLD = "button:has(svg path[d*='13 4H10C8.1'])"
    ITALIC = 'button:has(svg path[d="M12 4H19"])'
    UNDERLINE = "button:has(svg path[d*='M5.5 3V11.5C5.5'])"
    BULLET_POINTS = "button:has(svg path[d*='M8 5.5H20']):has(svg path[d*='M8 12.5H20'])"
    NUMERIC_POINTS =  "button:has(svg path[d='M11 6H21']):has(svg path[d='M11 12H21']):has(svg path[d='M11 18H21'])"
    LINK = "button:has(svg path[d*='M16.8463 14.6095L19.4558'])"
    AUDIO = "button:has(svg path[d*='M12.0009 19C15.0764 19 17.7195'])"
    PAUSE = "button:has(svg path[d*='M2.66406 4.66663C2.66406 3.72382 2.66406 3'])"
    CONTINUE = "button[data-slot='button'][data-variant='default'][data-size='icon-xs'][data-icon-only='true']"
    AUDIO_TICK = "button:has(svg path[d='M20 7L9 18L4 13'])"
    MULTIPLE_OPTIONS = "button:has(svg path[d*='M17 13.75V3.75M17 13.75C18.7956 13.75 20.25 15.2044 20.25 17C20.25 18.7956 18.7956 20.25 17'])"
    USER_INFO = 'button:has(svg path[d*="8.17157"])'
    TAG_SVG ="button:has(svg path[d*='M12 6.75V12M12 12V17.25M12 12H6'])"
    
    
    
    
    
    
    def wait(self, duration='medium'):
       
        self.page.wait_for_timeout(self.TIMEOUTS.get(duration, 1000))
        return self
    
    def go_to_inbox(self):
        self.page.wait_for_selector(self.INBOX_PAGE, state="visible", timeout=900000)
        self.page.click(self.INBOX_PAGE)
        self.page.wait_for_load_state("load")
        self.wait('short')
        self.page.locator("body").hover() 
        self.wait('short')
        self.click(self.PERSON_SVG)
        self.wait('medium')      
        
    def select_convo(self):
        self.page.locator("p:has-text('uzumymw')").click()
        self.wait('medium')
        
    def type_message(self,text="This is test message"):
        editor = self.page.locator('[contenteditable="true"][role="textbox"]')
        editor.wait_for(state="visible", timeout=5000)
        editor.click()
        editor.fill(text)

    def send_message(self):
        self.click(self.SEND_BTN)
        self.wait('medium')
        return self
    
    def inbox_actions(self):
        self.click(self.FORMATTING)
        self.wait('short')
        self.type_message("This is formatted text")
        self.page.keyboard.press("Control+A")
        
        self.click(self.BOLD)
        self.click(self.ITALIC)
        self.click(self.UNDERLINE)
        self.send_message()
        
    
        self.type_message("In bullet points")
        self.page.keyboard.press("Control+A")
        self.page.locator(self.BULLET_POINTS).click()
        self.click(self.SEND_BTN)
        self.wait('medium')
        
        self.type_message("In numeric points")
        self.page.keyboard.press("Control+A")
        self.click(self.NUMERIC_POINTS)
        self.click(self.SEND_BTN)
        self.wait('medium')
        #
        ##Link.........
        self.click(self.LINK)
        self.page.get_by_placeholder("Text to display").fill("This is link test....")
        self.wait('short')
        link_input = self.page.locator("input[value='https://']")
        link_input.click()
        link_input.press("Control+A")
        link_input.type("https://example.com")
        self.wait('medium')
        self.page.locator("button:has-text('Insert')").click()
        self.send_message()
        #
        ##Audio........
        self.click(self.AUDIO)
        self.wait('short')
        self.click(self.PAUSE)
        self.wait('long')
        self.click(self.CONTINUE)
        self.wait('short')
        self.click(self.AUDIO_TICK)
        self.wait('long')
        self.send_message()
        
        #Attachements.......
        self.click(self.MULTIPLE_OPTIONS)
        self.wait('medium')      

        # Click Add attachment and handle file chooser
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_role("menuitem", name="Add attachment").click()

        # Select files
        file_chooser = fc_info.value
        file_chooser.set_files([
            "/home/unique/Downloads/file1.pdf",
            "/home/unique/Downloads/file2.pdf",
            "/home/unique/Downloads/file3.pdf",
            "/home/unique/Downloads/20260805062609_cea0b22f.jpeg"
        ])
        self.wait('verylong')
        self.send_message()
   
    def note(self):
        self.page.locator("button:has-text('Reply')").click()
        self.wait('short')
        self.page.get_by_text("Notes(Internal Only)").click()
        self.wait('short')
        self.type_message("This is note")
        self.send_message()
        self.wait('long')
        #Edit
        self.page.locator("div:has-text('This is note')").last.hover()
        self.wait('long')
        self.click(self.MESSAGE_ACTION_SVG)
        self.page.get_by_role("menuitem", name="Edit").click()
        
        self.type_message("This is edited note........")
        self.send_message()
        #delete
        self.page.locator("div:has-text('This is edited note........')").last.hover()
        self.wait('long')
        self.click(self.NOTE_ACTION_SVG)
        self.page.get_by_role("menuitem", name="Delete").click()
        self.wait('short')
        
        self.page.locator("button:has-text('Confirm text')").click()
        self.wait('long')
    
    def quick_response(self):
        # Generate random values using BasePage method
        random_title = self.generate_random_text(8)
        random_shortcut = self.generate_random_text(6).lower()  # Lowercase for shortcut
        random_content = self.generate_random_text(12)
        
        self.page.locator("button:has-text('Quick Response')").click()
        self.page.locator("button:has-text('Add Quick Reply')").click()
        self.page.locator("#title").fill(random_title)
        self.page.locator("button:has-text('Select group')").click()
        self.wait('medium')
        self.page.get_by_role("option", name="Grouuup").click()
        self.wait('short')
        
        
        
        self.page.locator("#shortcut").fill(random_shortcut)
        self.wait('short')
        self.page.locator("#content").fill(random_content)
        
        print(f"✅ Created: Title='{random_title}', Shortcut='{random_shortcut}', Content='{random_content}'")
        return {
            'title': random_title,
            'shortcut': random_shortcut,
            'content': random_content
        }
        
    def create_quick_reply(self):
        self.page.locator("button:has-text('Create Quick Reply')").click()
    
    def private_response(self):
        result = self.quick_response()
        self.page.get_by_role("switch").click()
        self.create_quick_reply()
        print("Private quick response created")
        return result
     
    def inbox_reply(self):
         #reply
                self.type_message("This is for reply")
                self.send_message()
                self.page.locator("div:has-text('This is for reply')").last.hover()
                self.wait('long')
                self.click(self.MESSAGE_ACTION_SVG)
                self.page.get_by_role("menuitem", name="Reply").click()
                self.wait('short')
                self.type_message("Replied text......")
                self.send_message()
    
    def resolve_unresolve(self):
        self.page.locator("button:has-text('Unresolved')").click()
        self.wait('short')
        self.page.locator("#subject").fill("This is subject....")
        self.page.locator("#remarks").fill("This is remarks demo because it's demo ...")
        self.wait('medium')
        self.page.locator("button[type='submit']:has-text('Resolve')").click()
        #Take conversation........
        self.page.locator("button:has-text('Takeover Conversation')").click()
        
    def set_reminder(self):
        
        self.page.locator("//button[contains(text(), 'Set Reminder')]").click()
        self.wait('short')
        self.page.locator("button:has-text('Tomorrow')").click()
        self.page.locator("button:has-text('Set Date & time')").click()
        self.page.get_by_placeholder("Add reminder note").fill("This is reminder note...")
        self.send_message()
        
    def right_side(self):
        #User information
        self.click(self.USER_INFO)
        self.page.locator("#name").fill("uzumymw")
        self.page.locator("#email").fill("demo@email.com")
        self.page.locator("#phone").fill("7759802222")
        self.page.locator("button:has-text('Save')").click()
        
        #Lead
        self.page.locator("button:has-text('Lead Type')").first.click()
        self.wait('long')
        self.page.locator("button:has-text('Potential'), button:has-text('Non-potential')").click()
        self.wait('long')
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")
        
        #Tags......
        try:
            self.page.locator("button:has-text('Add Tags')").click()
            self.click(self.TAG_SVG)
            tag_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            self.page.get_by_placeholder("search or create tag").fill(tag_name)
            self.page.keyboard.press("Enter")
            print("Tag created successfully...")
            self.page.get_by_placeholder("search or create tag").fill(tag_name)
            self.page.keyboard.press("Enter")
            print("Tag used successflly....")
            self.page.keyboard.press("Escape")
        except Exception as e:
            print(f"Failed to create tag... Error: {e}")
            
        #Company details..........
        try:
            self.page.locator("button:has-text('Company Details')").click()
            self.page.locator("#company_name").fill("Demo company name")
            print("Company name filled...")
            
            #Company size
            self.page.locator("#company_size").click()
            self.page.keyboard.press("ArrowDown")
            self.page.keyboard.press("ArrowDown")
            self.page.keyboard.press("Enter")
            print("Company size selected...")
            
            #Industry
            self.page.locator("#company_industry").click()           
            self.page.keyboard.press("ArrowDown")          
            self.page.keyboard.press("ArrowDown")          
            self.page.keyboard.press("Enter")          
            print("Company industry selected......")     
            
            #Company website url 
            url = self.page.locator("#company_website_url")       
            url.click()           
            url.press("Control+A")        
            url.fill("https://thisdemowebsite.com")           
            print("URL inserted....")            
            
            #Other details.........
            other_details = self.page.locator("#other_details")          
            other_details.press("Control+A")
            other_details.fill("This is other company detail..")
            
        
        except Exception as e:
            print("Error in company details........")
        
       # #Notes
        #self.page.locator("button:has-text('Notes')").click()
                
       # #AI summary
       # self.page.locator("button:has-text('AI Summary')").click()
       # 
       # #Visit Information
       # self.page.locator("button:has-text('Visit Information')").click()
       # 
       # #AI Insights
       # self.page.locator("button:has-text('AI Insights')").click()
        
        #Reminder
        self.page.locator("button:has-text('Reminder')").first.click()
        #self.page.locator("div.flex.flex-col.gap-2.p-2.max-h-80 > div:first-child").click()
        self.page.locator("button:has-text('Mark as completed')").click()
        self.wait('short')
        self.page.locator("button:has-text('Close')").click()
        
        
        
        
                
        
        

        
        
        
        
        
        
        
        
        

        
    
    