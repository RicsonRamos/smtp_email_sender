import time
import streamlit as st
from core.smtp_client import connect, disconnect
from core.email_builder import build_message
from core.contacts import load_contacts, remove_contact, save_finished_contact
from core.rate_limit import RateLimiter
from core.retry import wait_for_retry
from utils.logger import log_event
from config.limits import DAILY_LIMIT
from utils.helpers import ensure_directory, clean_text
from config.content import SENDER_NAME

def run_campaign(status_container):
    """
    Orchestrates the email campaign and updates the Streamlit UI in real-time.
    """
    # 1. Environment Setup
    ensure_directory("data")
    ensure_directory("logs")
    
    limiter = RateLimiter()
    contacts = load_contacts()
    
    if not contacts:
        status_container.error("⚠️ No contacts found in the database.")
        return

    total_contacts = len(contacts)
    progress_bar = st.progress(0)
    log_area = st.empty() # Placeholder for dynamic status updates
    
    server = None
    try:
        status_container.info("🔄 Connecting to SMTP server...")
        server = connect()
        
        for index, contact in enumerate(contacts):
            # Update Progress Bar
            current_progress = (index) / total_contacts
            progress_bar.progress(current_progress)
            
            # Check Daily Quota
            if not limiter.can_send():
                status_container.warning(f"🛑 Daily limit of {DAILY_LIMIT} reached.")
                break
            
            # Data Sanitization
            company = clean_text(contact.get('company'))
            email = clean_text(contact.get('email'))

            if not email:
                log_event(f"Skipping empty email at index {index}")
                continue

            log_area.info(f"📧 Sending to: **{company}** <{email}>")
            
            # Execute Single Send
            success, error = send_single_email(server, company, email)
            
            if success:
                save_finished_contact(company, email, "SUCCESS")
                remove_contact(company, email)
                limiter.register_send()
                st.toast(f"✅ Success: {company}")
                
                # Intelligent Pacing
                if index < total_contacts - 1:
                    with st.spinner("⏳ Waiting for rate limit pacing..."):
                        limiter.wait()
            else:
                save_finished_contact(company, email, "FAILED", error=error)
                st.error(f"❌ Failed: {company} - {error}")

        # Finalize Progress
        progress_bar.progress(1.0)
        log_area.empty()
        
    except Exception as e:
        error_msg = f"🔥 Critical failure during campaign: {e}"
        st.error(error_msg)
        log_event(error_msg)
    finally:
        if server:
            disconnect(server)
            status_container.success("🏁 Connection closed. Campaign finished!")

def send_single_email(server, company, email):
    """
    Handles internal retries for a single email delivery attempt.
    """
    attempts = 0
    max_retries = 3
    
    while attempts < max_retries:
        try:
            # Using the centralized SENDER_NAME (Spock)
            msg = build_message(company, email, SENDER_NAME) 
            if msg:
                server.send_message(msg)
                return True, None
        except Exception as e:
            attempts += 1
            log_event(f"Attempt {attempts} failed for {company}: {e}")
            if attempts < max_retries:
                # Randomized wait time between retries
                wait_for_retry(attempts)
            else:
                return False, str(e)
    return False, "Maximum retries reached"
