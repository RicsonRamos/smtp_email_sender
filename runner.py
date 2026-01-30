import time
from core.smtp_client import connect, disconnect
from core.email_builder import build_message
from core.contacts import load_contacts, remove_contact, save_finished_contact
from core.rate_limit import RateLimiter
from core.retry import wait_for_retry
from utils.logger import log_event
from config.limits import DAILY_LIMIT

def run_campaign():
    """
    Orchestrates the email sending process: 
    loads contacts, builds messages, sends them sequentially, 
    and handles rate limits and retries.
    """
    limiter = RateLimiter()
    contacts = load_contacts()
    
    if not contacts:
        log_event("⚠️ No contacts found in the pending list. Aborting.")
        return

    total_contacts = len(contacts)
    log_event(f"📊 {total_contacts} contacts loaded. Daily limit is {DAILY_LIMIT}.")

    server = None
    try:
        # Start SMTP Connection
        server = connect()
        
        # Using enumerate to track the current index for the 'last-email' check
        for index, contact in enumerate(contacts):
            
            # 1. Check if we hit the 50-email daily cap
            if not limiter.can_send():
                log_event(f"🛑 Daily limit of {DAILY_LIMIT} reached. Stopping campaign for today.")
                break
            
            company = contact['company']
            email = contact['email']

            # 2. Attempt to send the email
            success, error = send_single_email(server, company, email)
            
            # 3. Process Results
            if success:
                save_finished_contact(company, email, "SUCCESS")
                remove_contact(company, email)
                limiter.register_send()
                log_event(f"✅ {limiter.get_status()}")

                # 4. Smart Wait: Only wait if there are more contacts to process
                if index < total_contacts - 1:
                    limiter.wait()
                else:
                    log_event("🏁 Last contact reached. Closing application immediately.")
            else:
                # Log failure but continue to the next contact
                save_finished_contact(company, email, "FAILED", error=error)
                log_event(f"❌ Permanent failure for {company} ({email}): {error}")

    except Exception as e:
        log_event(f"🔥 Critical failure during campaign execution: {e}")
    finally:
        if server:
            disconnect(server)

def send_single_email(server, company, email):
    """
    Handles the building and sending of one email, including internal retries.
    Returns: (bool success, str error_message)
    """
    attempts = 0
    max_retries = 3
    
    while attempts < max_retries:
        try:
            # Note: Using your name 'Spoke' for the template
            msg = build_message(company, email, "Spoke")
            if msg:
                server.send_message(msg)
                return True, None
        except Exception as e:
            attempts += 1
            log_event(f"🔄 Attempt {attempts} failed for {company}: {e}")
            if attempts < max_retries:
                wait_for_retry(attempts)
            else:
                return False, str(e)
    
    return False, "Maximum retries reached"

if __name__ == "__main__":
    run_campaign()