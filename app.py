import streamlit as st
import pandas as pd
import os
from runner import run_campaign
from config.content import SENDER_NAME, EMAIL_SUBJECT, EMAIL_BODY_TEXT

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Spock's SMTP Automator",
    page_icon="🖖",
    layout="wide"
)

# --- HELPER FUNCTIONS ---
def save_content_changes(new_subject, new_body, new_sender):
    """
    Saves the current UI state back to config/content.py using repr() 
    to prevent syntax errors with quotes or special characters.
    """
    content_path = "config/content.py"
    try:
        with open(content_path, "w", encoding="utf-8") as f:
            f.write("# Auto-generated configuration file\n")
            f.write(f'EMAIL_SUBJECT = {repr(new_subject)}\n')
            f.write(f'SENDER_NAME = {repr(new_sender)}\n')
            f.write(f'EMAIL_BODY_TEXT = {repr(new_body)}\n')
        return True
    except Exception as e:
        st.error(f"Error saving preferences: {e}")
        return False

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextArea textarea { font-family: 'Courier New', Courier, monospace; font-size: 14px; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>📧 Smart & Resilient SMTP Automator</h1>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #555; margin-bottom: 20px;'>
        This <b>High-Precision Email Engine</b> is designed for high-deliverability outreach. <br>
        Features dynamic template injection and a resilient retry mechanism.
        <br><i>Simply configure, upload, and launch.</i> 🖖
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR: AUTHENTICATION & TOOLS ---
with st.sidebar:
    st.header("🔐 Authentication")
    st.info("Credentials are used only for this session.")
    
    ui_sender_name = st.text_input("Sender Display Name", value=SENDER_NAME, placeholder="Commander Spock")
    sender_email = st.text_input("Sender Email", placeholder="spock@starfleet.fed.us")
    app_password = st.text_input("Google App Password", type="password", help="16-digit code from Google Security.", placeholder="🖖 live-long-and-prosper")
    
    st.divider()
    st.markdown("### 🛠️ System Tools")
    
    # Tool 1: Save Defaults
    if st.button("💾 Save as Default Settings", use_container_width=True):
        # These variables come from the main UI inputs (subject and body)
        if save_content_changes(st.session_state.get('subject_input', EMAIL_SUBJECT), 
                               st.session_state.get('body_input', EMAIL_BODY_TEXT), 
                               ui_sender_name):
            st.success("Preferences saved to content.py!")

    # Tool 2: Clean History
    if st.button("🗑️ Clean Finished History", use_container_width=True):
        if os.path.exists("data/finished.csv"):
            os.remove("data/finished.csv")
            st.rerun()

    st.divider()
        
    with st.expander("❓ Quick Setup Guide"):
        st.markdown("""
            **1. Google App Password**
            - Generate a 16-character code in Google Account Security.
            **2. CSV Format**
            - Needs `company` and `email` columns.
            **3. Dynamic Tags**
            - `{company}` and `{sender_name}`.
        """)

    st.link_button("📖 View Full README", "https://github.com/RicsonRamos/smtp_email_sender/blob/main/readme.md", use_container_width=True)

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Dynamic Template")
    
    # We use session_state keys to ensure the sidebar "Save" button can access current values
    subject = st.text_input(
        "Subject Line", 
        value=EMAIL_SUBJECT,
        key="subject_input"
    )
    
    st.markdown("<small>💡 <b>Tags:</b> <code>{company}</code>, <code>{sender_name}</code></small>", unsafe_allow_html=True)
    
    body = st.text_area(
        "Email Body", 
        value=EMAIL_BODY_TEXT, 
        height=400,
        key="body_input"
    )

with col2:
    st.subheader("📁 File Management")
    uploaded_files = st.file_uploader("Upload contacts (CSV) or Attachments", 
                                    type=["csv", "pdf", "docx"], 
                                    accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension == "csv":
                save_path = os.path.join("data", "contacts.csv")
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"✅ Database updated: `{uploaded_file.name}`")
            else:
                save_path = os.path.join("attachments", uploaded_file.name)
                os.makedirs("attachments", exist_ok=True)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.toast(f"📎 Attached: {uploaded_file.name}")

    if st.button("🗑️ Clear All Attachments"):
        if os.path.exists("attachments"):
            for f in os.listdir("attachments"):
                os.remove(os.path.join("attachments", f))
            st.rerun()

# --- EXECUTION ENGINE ---
st.divider()

if st.button("🚀 LAUNCH CAMPAIGN", use_container_width=True):
    if not sender_email or not app_password:
        st.error("❌ Authentication Required: Please fill in the sidebar fields.")
    elif not os.path.exists("data/contacts.csv"):
        st.error("❌ Data Missing: No contacts found to process.")
    else:
        os.environ["SENDER_EMAIL"] = sender_email
        os.environ["APP_PASSWORD"] = app_password
        
        status_container = st.empty()
        with st.status("Initiating SMTP Protocols...", expanded=True) as status:
            run_campaign(status_container, subject, body, ui_sender_name)
            status.update(label="Campaign Sequence Completed!", state="complete", expanded=False)
        
        st.balloons()
        st.toast("Campaign Successful!", icon="🖖")

# --- ANALYTICS DASHBOARD ---
if os.path.exists("data/finished.csv"):
    st.divider()
    st.subheader("📊 Post-Campaign Intelligence")
    try:
        history_df = pd.read_csv("data/finished.csv")
        if 'status' in history_df.columns:
            m1, m2, m3 = st.columns(3)
            success_count = len(history_df[history_df['status'] == 'SUCCESS'])
            fail_count = len(history_df[history_df['status'] == 'FAILED'])
            
            m1.metric("Processed", len(history_df))
            m2.metric("Success", success_count, delta_color="normal")
            m3.metric("Failures", fail_count, delta_color="inverse")
            
            st.dataframe(history_df, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading analytics: {e}")