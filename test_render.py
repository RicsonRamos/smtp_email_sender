import os
from core.email_builder import build_message
from utils.logger import log_event

def run_dry_test():
    """
    Simulates email generation and saves the HTML output to a local file.
    Use this to verify layout, variables, and attachments before launching a campaign.
    """
    # Mock data for testing
    test_company = "Example Law Firm"
    test_email = "recruitment@example.com"
    test_sender = "Spoke"  # Your name variable

    log_event(" Starting Dry Run test...")

    # Build the message using the core engine
    msg = build_message(test_company, test_email, test_sender)

    if msg:
        # Extract the HTML part from the multipart message
        html_content = None
        
        # We iterate through the message parts to find the 'text/html' subtype
        for part in msg.iter_parts():
            if part.get_content_subtype() == 'html':
                html_content = part.get_payload(decode=True).decode('utf-8')
                break
        
        if html_content:
            # Save the rendered HTML to a local file
            output_filename = "test_output.html"
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            print("-" * 60)
            print("RENDER SUCCESS!")
            print(f"Subject: {msg['Subject']}")
            print(f"File Generated: '{output_filename}'")
            print("Open this file in your browser to verify the layout.")
            print("-" * 60)
            
            # Check and list detected attachments
            attachments = [part.get_filename() for part in msg.iter_attachments()]
            print(f"📎 Attachments detected: {attachments}")
        else:
            print(" Error: Could not find the HTML part within the generated email.")
    else:
        print(" Error: Message building failed. Check the logs for details.")

if __name__ == "__main__":
    run_dry_test()