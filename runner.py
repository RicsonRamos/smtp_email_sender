import time
from core.smtp_client import connect, disconnect
from core.email_builder import build_message
from core.contacts import load_contacts, remove_contact, save_finished_contact
from core.rate_limit import RateLimiter
from core.retry import wait_for_retry
from utils.logger import log_event
from config.limits import DAILY_LIMIT
# Importando os helpers refatorados
from utils.helpers import ensure_directory, clean_text

def run_campaign():
    """
    Orchestrates the email campaign with integrated sanitization and environment checks.
    """
    # 1. PRE-FLIGHT CHECKS: Ensure required directories exist
    ensure_directory("data")
    ensure_directory("logs")
    ensure_directory("attachments")

    limiter = RateLimiter()
    contacts = load_contacts()
    
    if not contacts:
        log_event("⚠️ No contacts found. Aborting.")
        return

    total_contacts = len(contacts)
    log_event(f"📊 {total_contacts} contacts loaded. Daily limit: {DAILY_LIMIT}.")

    server = None
    try:
        server = connect()
        
        for index, contact in enumerate(contacts):
            if not limiter.can_send():
                log_event(f"🛑 Daily limit of {DAILY_LIMIT} reached.")
                break
            
            # 2. DATA SANITIZATION: Cleaning company and email strings
            company = clean_text(contact.get('company'))
            email = clean_text(contact.get('email'))

            if not email:
                log_event(f"⚠️ Skipping invalid contact at index {index}")
                continue

            # 3. EXECUTION
            success, error = send_single_email(server, company, email)
            
            if success:
                save_finished_contact(company, email, "SUCCESS")
                remove_contact(company, email)
                limiter.register_send()
                log_event(f"✅ {limiter.get_status()}")

                if index < total_contacts - 1:
                    limiter.wait()
                else:
                    log_event("🏁 Last contact reached. Closing app.")
            else:
                save_finished_contact(company, email, "FAILED", error=error)
                log_event(f"❌ Permanent failure for {company}: {error}")

    except Exception as e:
        log_event(f"🔥 Critical failure: {e}")
    finally:
        if server:
            disconnect(server)

def send_single_email(server, company, email):
    """
    Handles internal retries for a single email attempt.
    """
    attempts = 0
    max_retries = 3
    
    while attempts < max_retries:
        try:
            # Personalization with 'Spoke'
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
    return False, "Max retries reached"

if __name__ == "__main__":
    run_campaign()
