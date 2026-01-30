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

def run_campaign(status_container, custom_subject, custom_body, sender_name):
    """
    Orchestrates the email campaign using dynamic content and UI inputs.
    """
    ensure_directory("data")
    ensure_directory("logs")
    
    limiter = RateLimiter()
    contacts = load_contacts()
    
    if not contacts:
        status_container.error("No contacts found in data/contacts.csv")
        return
    
    total = len(contacts)
    progress_bar = st.progress(0)
    log_area = st.empty()
    
    server = None
    try:
        log_event("Starting campaign via Streamlit UI")
        # Initial connection
        server = connect() 
        
        for index, contact in enumerate(contacts):
            # Update Streamlit progress bar
            progress_bar.progress((index) / total)
            
            if not limiter.can_send():
                status_container.warning(f"Daily limit of {DAILY_LIMIT} reached.")
                break
            
            company = clean_text(contact.get('company'))
            email = clean_text(contact.get('email'))

            if not email:
                continue

            log_area.info(f"📤 Sending to: **{company}** ({email})")
            
            # Attempt delivery; returns the server instance in case of reconnection
            success, error, server = send_single_email(
                server, company, email, custom_subject, custom_body, sender_name
            )
            
            if success:
                save_finished_contact(company, email, "SUCCESS")
                remove_contact(company, email)
                limiter.register_send()
                st.toast(f"✅ Sent: {company}")
                
                # Dynamic pacing to avoid spam filters
                if index < total - 1:
                    with st.spinner("⏳ Pacing..."):
                        limiter.wait()
            else:
                save_finished_contact(company, email, "FAILED", error=error)
                st.error(f"❌ Failed: {company} | Error: {error}")

        progress_bar.progress(1.0)
        log_area.success("🎯 Campaign sequence completed successfully!")
        
    except Exception as e:
        error_msg = f"Critical Engine Error: {e}"
        st.error(error_msg)
        log_event(error_msg)
    finally:
        if server:
            disconnect(server)

def send_single_email(server, company, email, subject, body, sender_name):
    """
    Handles building and sending with a retry mechanism and auto-reconnection.
    """
    attempts = 0
    max_retries = 3
    last_error = ""
    
    while attempts < max_retries:
        try:
            # Auto-reconnect if the server connection was lost or reset
            if server is None:
                server = connect()

            # Build the MIME message
            msg = build_message(company, email, sender_name, subject, body)
            
            if msg is None:
                return False, "Message build failed (Check template tags)", server
            
            server.send_message(msg)
            return True, None, server
            
        except Exception as e:
            attempts += 1
            last_error = str(e)
            log_event(f"Attempt {attempts} failed for {company}: {e}")
            
            # Force server reset to trigger reconnection on the next retry attempt
            server = None 
            
            if attempts < max_retries:
                wait_for_retry(attempts)
            
    return False, last_error, server