from pages.base_page import BasePage
import random
import string


class LeadAndCRMPage(BasePage):
    
    TIMEOUTS = {
        'short': 500,
        'medium': 1000,
        'long': 2000,
    }
    
    LEAD_AND_CRM = "//*[local-name()='svg' and .//*[local-name()='path' and contains(@d, 'M5.75 4.5H18.25')]]"
    LEAD_SVG = "//*[local-name()='svg' and .//*[local-name()='path' and contains(@d, 'M20.25 10.25V3.75H13.75M20.25 3.75L11 13')]]"
    
    def wait(self, duration='medium'):
        self.page.wait_for_timeout(self.TIMEOUTS[duration])
        return self

    def go_to_lead(self):
        self.page.wait_for_selector(self.LEAD_AND_CRM, state="visible", timeout=30000)
        self.page.click(self.LEAD_AND_CRM)
        self.page.wait_for_load_state("load")

    def open_new_lead(self):
        self.page.get_by_text("New Lead").click()
        self.page.get_by_placeholder("e.g. Jane Smith").wait_for(state="visible")
        return self

    def text_fields(self):
        return {
            "name": self.page.get_by_placeholder("e.g. Jane Smith"),
            "phone": self.page.get_by_placeholder("Enter Phone Number"),
            "email": self.page.locator("#email"),
            "location": self.page.locator("#address"),
            "referred_by": self.page.get_by_placeholder("Referred By"),
            "budget": self.page.locator("#budget"),
            "interest_area": self.page.locator("#interest_area"),
            "notes": self.page.get_by_placeholder(
                "Add any specific requirement here..."
            ),
        }

    def submit_lead(self):
        self.page.get_by_role("button", name="Add lead").click()
        return self 
    
    def create_lead(self):
        # Generate random data
        random_name = ''.join(random.choices(string.ascii_letters, k=random.randint(6, 10)))
        random_email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@test.com"
        random_phone = ''.join(random.choices(string.digits, k=10))
        random_budget = str(random.randint(1000, 50000))
        random_interest = ''.join(random.choices(string.ascii_letters, k=random.randint(8, 15)))
        random_referred = ''.join(random.choices(string.ascii_letters, k=random.randint(6, 10)))
        random_location = f"{random.randint(100, 999)} Main St, Anytown, USA"

        # Random lead type
        lead_types = ["SMB", "Enterprise", "Partner", "Support to Sales"]
        random_lead_type = random.choice(lead_types)

        # Random lead source
        lead_sources = [
            "Website Chat", "Live Visitor", "Contact Form", "Demo Request", 
            "Email", "Whatsapp", "Instagram", "Facebook", "Linkedin", 
            "Google Ads", "Organic Search", "Referral", "Event / Webinar", 
            "Manual entry"
        ]
        random_lead_source = random.choice(lead_sources)

        # Click New Lead button
        self.page.get_by_text("New Lead").click()
        self.wait('short')

        # Fill Name
        name_input = self.page.get_by_placeholder("e.g. Jane Smith")
        name_input.wait_for(state="visible")
        name_input.fill(random_name)

        # Fill Phone
        phone_input = self.page.get_by_placeholder("Enter Phone Number")
        self.wait('short')
        phone_input.fill(random_phone)

        # Fill Email
        email_input = self.page.locator('#email')
        self.wait('short')
        email_input.fill(random_email)

        # Fill Location
        location_input = self.page.locator('#address')
        self.wait('short')
        location_input.fill(random_location)

        # Select Lead Type - Random
        self.page.locator('#lead_type').click()
        self.wait('short')
        self.page.get_by_role("option", name=random_lead_type).click()

        # Select Lead Source - Random
        self.page.locator('#lead_source').click()
        self.wait('short')
        self.page.get_by_role("option", name=random_lead_source).click()

        # Fill Referred By
        referred = self.page.get_by_placeholder("Referred By")
        self.wait('short')
        referred.fill(random_referred)

        # Fill Budget
        budget = self.page.locator('#budget')
        self.wait('short')
        budget.fill(random_budget)

        # Fill Interest Area
        interest_area = self.page.locator('#interest_area')
        self.wait('short')
        interest_area.fill(random_interest)

        # Fill Notes
        notes = self.page.get_by_placeholder("Add any specific requirement here...")
        self.wait('short')
        notes.fill("This is a test lead created for automation testing purposes.")

        self.page.wait_for_load_state("load")

        # Click Add Lead button
        self.page.get_by_role("button", name="Add lead").click()

        self.page.wait_for_timeout(2000)
        
    def sort_by(self):
        self.page.locator("button:has-text('Sort')").click()
        
        self.page.get_by_role("option", name="Newest First").click()
        self.wait('long')
        self.page.locator("button:has-text('Newest First')").click()
        
        self.page.get_by_role("option", name="Oldest First").click()
        self.wait('long')
        self.page.locator("button:has-text('Oldest First')").click()
        
        self.page.get_by_role("option", name="Lead Name (A–Z)").click()
        self.wait('long')
        self.page.locator("button:has-text('Lead Name (A–Z)')").click()
        
        self.page.get_by_role("option", name="Lead Name (Z–A)").click()
        self.wait('long')
        self.page.locator("button:has-text('Lead Name (Z–A)')").click()
        
        self.page.get_by_role("option", name="Referred By").click()
        self.wait('long')   
        
    def filter_by(self):
        self.page.locator("button:has-text('All Statuses')").click()
                
        self.wait('long')
        self.page.get_by_role("option", name="New").click()
        self.wait('long')
        self.page.locator("button:has-text('New')").nth(1).click()
        self.wait('short')
        
        self.page.get_by_role("option", name="Contacted").click()
        self.wait('long')
        self.page.locator("button:has-text('Contacted')").click()
        self.wait('short')
        
        self.page.get_by_role("option", name="Qualified").click()
        self.wait('long')
        self.page.locator("button:has-text('Qualified')").click()
        self.wait('short')
        
        self.page.get_by_role("option", name="Proposal Sent ").click()
        self.wait('long')
        self.page.locator("button:has-text('Proposal Sent')").click()
        self.wait('short')
        
        self.page.get_by_role("option", name="Negotiation").click()
        self.wait('long')
        self.page.locator("button:has-text('Negotiation')").click()
        self.wait('short')
        
        self.page.get_by_role("option", name="Won").click()
        self.wait('long')
        self.page.locator("button:has-text('Won')").click()
        self.wait('short')
        
        self.page.get_by_role("option", name="Lost").click()
        self.wait('long')
    #Source filter
    def filter_by_source(self):
        self.page.locator("button:has-text('All Sources')").click()

        self.wait('long')
        self.page.get_by_role("option", name="Website Chat").click()
        self.wait('long')
        self.page.locator("button:has-text('Website Chat')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Live Visitor").click()
        self.wait('long')
        self.page.locator("button:has-text('Live Visitor')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Contact Form").click()
        self.wait('long')
        self.page.locator("button:has-text('Contact Form')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Demo Request").click()
        self.wait('long')
        self.page.locator("button:has-text('Demo Request')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Email").click()
        self.wait('long')
        self.page.locator("button:has-text('Email')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Whatsapp").click()
        self.wait('long')
        self.page.locator("button:has-text('Whatsapp')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Instagram").click()
        self.wait('long')
        self.page.locator("button:has-text('Instagram')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Facebook").click()
        self.wait('long')
        self.page.locator("button:has-text('Facebook')").click()
        self.wait('short')

        self.page.get_by_role("option", name="LinkedIn").click()
        self.wait('long')
        self.page.locator("button:has-text('LinkedIn')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Google Ads").click()
        self.wait('long')
        self.page.locator("button:has-text('Google Ads')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Organic Search").click()
        self.wait('long')
        self.page.locator("button:has-text('Organic Search')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Referral").click()
        self.wait('long')
        self.page.locator("button:has-text('Referral')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Event / Webinar").click()
        self.wait('long')
        self.page.locator("button:has-text('Event / Webinar')").click()
        self.wait('short')

        self.page.get_by_role("option", name="Manual entry").click()
        self.wait('long')

    def all_assignees(self):
        self.page.locator("button:has-text('All Assignees')").click()
        self.wait('short')
        
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")
        self.wait('short')
        
    def search_actions(self):
        self.page.locator("input[placeholder='Search Lead...']").click()
        self.wait('short')
        
        self.page.keyboard.type("Te")
        self.wait('short')
        self.click(self.LEAD_SVG)
        #Edit lead
        self.page.locator("button:has-text('Edit')").click()
        self.wait('short')
        self.page.locator('#interest_area').clear()
        self.page.locator('#interest_area').fill("Updated Interest Area")
        self.wait('short')
        
        self.page.locator('#budget').clear()
        self.page.locator('#budget').fill("43222")
        self.wait('short')

        self.page.locator('#referred_by').clear()
        self.page.locator('#referred_by').fill("Updated Referred By")
        self.wait('medium')
        
        button_texts = ["Qualified", "Proposal Sent", "Negotiation", "Won", "Lost"]
        
        random_button = random.choice(button_texts)

        # Click just one random button
        self.page.locator(f"button:has-text('{random_button}')").click()
        
        
        self.wait('medium')
        
        self.page.get_by_placeholder("Add internal notes about this lead...").clear()
        self.page.get_by_placeholder("Add internal notes about this lead...").fill("Updated internal notes for this lead.")
        
        self.page.locator("button:has-text('Update Status')").click()
        self.wait('long')
        self.wait('long')
        self.wait('long')
        self.wait('long')
        self.wait('long')
        
        


        
        
        