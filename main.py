from playwright.sync_api import sync_playwright

from utils.auth import authenticate, get_session_id
from utils.browser import create_context, launch_browser
from pages.Leadandcrm import LeadAndCRMPage
from pages.tickets import TicketPage
from pages.inbox import InboxPage


def main():
    session_id = get_session_id()
    
    with sync_playwright() as playwright:
        browser = launch_browser(playwright)
        context = create_context(browser, session_id)
        try:
            page = authenticate(context, session_id)
            #Inbox--------------------
            inbox = InboxPage(page)
            inbox.go_to_inbox()
            inbox.select_convo()
            #inbox.inbox_actions()
            #inbox.type_message()
            #inbox.send_message()
            #inbox.inbox_reply()
            #inbox.resolve_unresolve()
        #Note--------------------------
            #inbox.note()
        #Quick response----------------
            #inbox.quick_response()
            #inbox.create_quick_reply()
            #inbox.private_response()
            #inbox.set_reminder()
        #Right sidebar-----------------
            #inbox.right_side()
        
            
            
            
            
            
            #lead_page = LeadAndCRMPage(page)
            #
            #lead_page.go_to_lead()
            
            #for i in range(100):    
            #    lead_page.create_lead()
            #    
            #lead_page.sort_by()
            #lead_page.filter_by()
            #lead_page.filter_by_source()
            #lead_page.all_assignees()
            #lead_page.search_actions()
            
            #Tickets...............
            #ticket_page = TicketPage(page)
            #ticket_page.go_to_ticket()
            #
            #for i in range(50):
            #    ticket_page.create_ticket()
            #    ticket_page.fill_ticket_form()
            
            
            
            

        finally:
            print("Closing browser...")
            
            


if __name__ == "__main__":
    main()