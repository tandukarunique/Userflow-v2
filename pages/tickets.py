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
            'long': (1500, 3000),
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
        
        # Random phone number prefixes
        #self.phone_prefixes = ["332", "345", "356", "367", "378", "389", "390"]

    def wait(self, duration_type='short'):
        """Override wait method to use random times"""
        if duration_type in self.random_ranges:
            min_time, max_time = self.random_ranges[duration_type]
            wait_time = random.randint(min_time, max_time) / 1000  # Convert to seconds
            time.sleep(wait_time)
        else:
            # Fallback to original wait times
            time.sleep(self.wait_times.get(duration_type, 500) / 1000)
    
    def go_to_ticket(self):
        self.page.locator(TICKET_LINK).click()
        self.wait('long')
        
    def create_ticket(self):
        self.page.locator("button:has-text('Create Ticket')").click()
        self.wait('medium')
        
    def fill_ticket_form(self):
        # Scope selection (randomly select or use first)
        self.page.locator('#scopeUuid').click()
        self.wait('short')
        self.page.press('#scopeUuid', 'Enter')
        self.wait('short')
        
        # Email - random generation
        random_email = f"user{random.randint(1000, 9999)}{random.choice(self.email_domains)}"
        self.page.locator('#email').fill(random_email)
        self.wait('long')
        
        # Fullname - random names
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emma", "Robert", "Lisa", "James", "Maria"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        random_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        self.page.get_by_placeholder("Enter full name...").fill(random_name)
        self.wait('short')
        
       
        
        # Address - random addresses
        streets = ["Main St", "Oak Ave", "Pine Rd", "Maple Dr", "Cedar Ln", "Elm Blvd", "Park Ave", "Lake St"]
        cities = ["Springfield", "Riverside", "Oakland", "Brooklyn", "Denver", "Austin", "Seattle", "Miami"]
        random_address = f"{random.randint(100, 999)} {random.choice(streets)}, {random.choice(cities)}"
        self.page.get_by_placeholder("Enter address...").fill(random_address)
        self.wait('short')
        
        # Source
        self.page.locator('#source').click()
        self.wait('short')
        self.page.press('#source', 'ArrowDown')     
        self.wait('short')
        self.page.press('#source', 'Enter')
        self.wait('short')
        
        # Ticket Subject - random subjects
        subjects = [
            "Test Ticket Subject",
            "Customer Inquiry",
            "Technical Support Request",
            "Billing Question",
            "Feature Suggestion",
            "Account Issue",
            "Bug Report",
            "General Assistance"
        ]
        self.page.locator('#subject').fill(random.choice(subjects))
        self.wait('short')
        
        # Category - randomly selected from all options
        category_choice = random.choice(self.category_options)
        self.page.locator('#category').click()
        self.wait('short')
        self.page.get_by_role("option", name=category_choice).click()
        self.wait('short')
        
        # Status - randomly selected from all options
        status_choice = random.choice(self.status_options)
        self.page.locator('#status').click()
        self.wait('short')
        self.page.get_by_role("option", name=status_choice).click()
        self.wait('short')
        
        # Priority - randomly selected from all options
        priority_choice = random.choice(self.priority_options)
        self.page.locator('#priority').click()
        self.wait('short')      
        self.page.get_by_role("option", name=priority_choice).click()
        self.wait('short')
        
        # Team - sometimes select, sometimes skip
        self.page.locator('#teamUuid').click()
        self.wait('short')
        self.page.press('#teamUuid', 'ArrowDown')
        self.wait('short')
        self.page.press('#teamUuid', 'Enter')
        self.wait('short')
        
        # Assignees - sometimes select, sometimes skip
        self.page.locator('#assignees').click()
        self.wait('short')      
        self.page.press('#assignees', 'ArrowDown')
        self.wait('short')
        self.page.press('#assignees', 'Enter')
        self.wait('short')  
        
        # Tags - random tag generation
        tags = ["Test", "Urgent", "Customer", "Technical", "Billing", "Feature", "Bug", "Enhancement"]
        random_tag = random.choice(tags)
        self.page.locator('#tags').fill(random_tag)
        self.wait('short')      
        self.page.press('#tags', 'Enter')   
        self.wait('short')
        
        # Description - random descriptions
        descriptions = [
            "Test Ticket Description",
            "Customer reported an issue with the application",
            "Requesting assistance with billing concerns",
            "Suggestion for improving user experience",
            "Technical problem encountered during login",
            "Account-related question requiring support"
        ]
        self.page.locator('#description').fill(random.choice(descriptions))
        self.wait('short')  
        
        # Internal notes - random notes
        notes = [
            "Test Ticket Internal Notes",
            "Initial investigation required",
            "Escalate to senior team member",
            "Customer needs urgent response",
            "Scheduled for follow-up review"
        ]
        self.page.locator('#note').fill(random.choice(notes))
        self.wait('short')
        
        # Create ticket button
        self.page.locator('button:has-text("Create Ticket")').last.click()
        self.wait('long')
        
    def fill_ticket_form_with_specific_values(self, 
                                             category=None, 
                                             status=None, 
                                             priority=None,
                                             name=None,
                                             email=None):
        """Optional method to fill form with specific values while keeping random wait times"""
        
        # Use provided values or random ones
        self.page.locator('#scopeUuid').click()
        self.wait('short')
        self.page.press('#scopeUuid', 'Enter')
        self.wait('short')
        
        # Email
        if email:
            self.page.locator('#email').fill(email)
        else:
            random_email = f"user{random.randint(1000, 9999)}{random.choice(self.email_domains)}"
            self.page.locator('#email').fill(random_email)
        self.wait('long')
        
        # Fullname
        if name:
            self.page.get_by_placeholder("Enter full name...").fill(name)
        else:
            first_names = ["John", "Jane", "Michael", "Sarah"]
            last_names = ["Smith", "Johnson", "Williams", "Brown"]
            self.page.get_by_placeholder("Enter full name...").fill(f"{random.choice(first_names)} {random.choice(last_names)}")
        self.wait('short')
        
       
        
        # Address
        streets = ["Main St", "Oak Ave", "Pine Rd", "Maple Dr"]
        cities = ["Springfield", "Riverside", "Oakland", "Brooklyn"]
        random_address = f"{random.randint(100, 999)} {random.choice(streets)}, {random.choice(cities)}"
        self.page.get_by_placeholder("Enter address...").fill(random_address)
        self.wait('short')
        
        # Source
        self.page.locator('#source').click()
        self.wait('short')
        self.page.press('#source', 'ArrowDown')     
        self.wait('short')
        self.page.press('#source', 'Enter')
        self.wait('short')
        
        # Subject
        self.page.locator('#subject').fill(f"Test Subject {''.join(random.choices(string.ascii_lowercase, k=4))}")
        self.wait('short')     
           
        # Category - use specified or random
        category_choice = category if category else random.choice(self.category_options)
        self.page.locator('#category').click()
        self.wait('short')
        self.page.get_by_role("option", name=category_choice).click()
        self.wait('short')
        
        # Status - use specified or random
        status_choice = status if status else random.choice(self.status_options)
        self.page.locator('#status').click()
        self.wait('short')
        self.page.get_by_role("option", name=status_choice).click()
        self.wait('short')
        
        # Priority - use specified or random
        priority_choice = priority if priority else random.choice(self.priority_options)
        self.page.locator('#priority').click()
        self.wait('short')      
        self.page.get_by_role("option", name=priority_choice).click()
        self.wait('short')
        
        # Rest of the form...
        self.page.locator('#teamUuid').click()
        self.wait('short')
        self.page.press('#teamUuid', 'ArrowDown')
        self.wait('short')
        self.page.press('#teamUuid', 'Enter')
        self.wait('short')
        
        self.page.locator('#assignees').click()
        self.wait('short')      
        self.page.press('#assignees', 'ArrowDown')
        self.wait('short')
        self.page.press('#assignees', 'Enter')
        self.wait('short')  
        
        self.page.locator('#tags').fill("Test Tag")
        self.wait('short')      
        self.page.press('#tags', 'Enter')   
        self.wait('short')
        
        self.page.locator('#description').fill("Test Description")
        self.wait('short')  
        
        self.page.locator('#note').fill("Test Note")
        self.wait('short')
        
        self.page.locator('button:has-text("Create Ticket")').last.click()
        self.wait('long')