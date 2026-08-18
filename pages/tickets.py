from playwright.sync_api import Page
import time
import random
import string

from pages.Leadandcrm import LeadAndCRMPage

TICKET_LINK = "//*[local-name()='svg' and .//*[local-name()='path' and contains(@d, 'M19 4.99902H5C3.89543 4.99902')]]"

class TicketPage(LeadAndCRMPage):
    def __init__(self, page: Page):
        self.page = page
        # Base wait times
        self.wait_times = {
            'short': 500,
            'medium': 1000,
            'long': 2000,
        }
        
        # Random range for each wait time (min, max) in milliseconds
        self.random_ranges = {
            'short': (300, 800),
            'medium': (800, 1500),
            'long': (15000, 90000),
        }
        
        # Category options
        self.category_options = [
            "General", "Billing & payment", "Technical Issue", 
            "Login Issue", "Account Management", "Bug Report", 
            "Feature Request", "Integration Issue", "Subscription plan", 
            "Refund Request", "General Support"
        ]
        
        # Status options
        self.status_options = [
            "Open", "In Progress", "Pending", "Waiting for Customer", 
            "Waiting for Internal Team", "Escalated", "Resolved", 
            "Closed", "Archived"
        ]
        
        # Priority options
        self.priority_options = ["Low", "Medium", "High", "Urgent"]
        
        # Random email domains for variety
        self.email_domains = ["@test.com", "@example.com", "@demo.net", "@sample.org", "@fake.mail"]
        
    def wait(self, duration_type='short'):
        """Override wait method to use random times"""
        if duration_type in self.random_ranges:
            min_time, max_time = self.random_ranges[duration_type]
            wait_time = random.randint(min_time, max_time) / 1000  # Convert to seconds
            time.sleep(wait_time)
        else:
            # Fallback to original wait times
            time.sleep(self.wait_times.get(duration_type, 500) / 1000)

    def random_string(self, length=8):
        """Generate a random alphabetic string, e.g. for tags"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def go_to_ticket(self):
        self.page.locator(TICKET_LINK).click()
        self.wait('short')
        
    def create_ticket(self):
        self.page.locator("button:has-text('Create Ticket')").first.click()
        
        
    def fill_ticket_form(self):
        self.page.locator('#scopeUuid').click()
        self.page.press('#scopeUuid', 'Enter')
    
        random_email = f"user{random.randint(1000, 9999)}{random.choice(self.email_domains)}"
        self.page.locator('#email').fill(random_email)
        
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emma", "Robert", "Lisa", "James", "Maria"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        random_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        self.page.get_by_placeholder("Enter full name...").fill(random_name)
        
        streets = ["Main St", "Oak Ave", "Pine Rd", "Maple Dr", "Cedar Ln", "Elm Blvd", "Park Ave", "Lake St"]
        cities = ["Springfield", "Riverside", "Oakland", "Brooklyn", "Denver", "Austin", "Seattle", "Miami"]
        random_address = f"{random.randint(100, 999)} {random.choice(streets)}, {random.choice(cities)}"
        self.page.get_by_placeholder("Enter address...").fill(random_address)
        
        self.page.locator('#source').click()
        self.page.press('#source', 'ArrowDown')     
        self.page.press('#source', 'Enter')
        
        self.page.locator('#subject').fill(self.random_string(random.randint(6, 15)))
       
        category_choice = random.choice(self.category_options)
        self.page.locator('#category').click()
        self.page.get_by_role("option", name=category_choice).click()
      
        status_choice = random.choice(self.status_options)
        self.page.locator('#status').click()
        self.wait('short')
        self.page.get_by_role("option", name=status_choice).click()
      
        priority_choice = random.choice(self.priority_options)
        self.page.locator('#priority').click()  
        self.page.get_by_role("option", name=priority_choice).click()
       
        self.page.locator('#teamUuid').click()
        self.page.press('#teamUuid', 'ArrowDown')
        self.page.press('#teamUuid', 'Enter')
        
        self.page.locator('#assignees').click()   
        self.page.press('#assignees', 'ArrowDown')
        self.page.press('#assignees', 'Enter')
    
        random_tag = self.random_string(8)
        self.page.locator('#tags').fill(random_tag)      
        self.page.press('#tags', 'Enter')  
        
        descriptions = [
            "Test Ticket Description",
            "Customer reported an issue with the application",
            "Requesting assistance with billing concerns",
            "Suggestion for improving user experience",
            "Technical problem encountered during login",
            "Account-related question requiring support"
        ]
        self.page.locator('#description').fill(random.choice(descriptions))
        
        notes = [
            "Test Ticket Internal Notes",
            "Initial investigation required",
            "Escalate to senior team member",
            "Customer needs urgent response",
            "Scheduled for follow-up review"
        ]
        self.page.locator('#note').fill(random.choice(notes))
        
    
    def attachments(self):
        import os
        
        # Files to upload
        files_to_upload = [
            "/home/unique/Downloads/file1.pdf",
            "/home/unique/Downloads/file2.pdf",
            "/home/unique/Downloads/file3.pdf",
            "/home/unique/Downloads/20260805062609_cea0b22f.jpeg"
        ]
        
        # Check which files exist
        valid_files = [f for f in files_to_upload if os.path.exists(f)]
        
        if not valid_files:
            print("No valid files found")
            self.page.locator('button:has-text("Create Ticket")').last.click()
            return
        
        upload_success = False
        
        # Try direct file input
        try:
            file_input = self.page.locator('input[type="file"]').first
            if file_input.count() > 0:
                file_input.set_input_files(valid_files)
                upload_success = True
                self.wait('medium')
        except:
            pass
        
        # Try button click approach if direct input failed
        if not upload_success:
            try:
                drop_zone = self.page.get_by_role('button', name='Drag and drop files here, or activate to browse for files')
                if drop_zone.count() > 0:
                    drop_zone.click()
                    self.wait('short')
                
                with self.page.expect_file_chooser() as fc_info:
                    attachment_btn = self.page.get_by_role("menuitem", name="Add attachment")
                    if attachment_btn.count() == 0:
                        attachment_btn = self.page.locator('button:has-text("Add attachment")').first
                    attachment_btn.click()
                
                file_chooser = fc_info.value
                file_chooser.set_files(valid_files)
                upload_success = True
                self.wait('short')
            except:
                pass
            
        # Click Create Ticket
        self.page.locator('button:has-text("Create Ticket")').last.click()
        self.wait('short')