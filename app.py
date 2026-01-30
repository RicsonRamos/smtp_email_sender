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

# --- CUSTOM CSS FOR BETTER UI ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #2980b9;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("📧 Smart & Resilient SMTP Automator")
st.markdown(f"**Welcome, {SENDER_NAME}.** Use this dashboard to manage your professional email campaigns.")

# --- SIDEBAR: CREDENTIALS & SECURITY ---
with st.sidebar:
    st.header("🔐 Authentication")
    st.info("Your credentials are used only for the current session and are not stored permanently.")
    
    email_user = st.text_input("Sender Email", placeholder="your-email@gmail.com")
    email_pass = st.text_input("Google App Password", type="password", help="16-digit password generated in Google Security settings.")
    
    st.divider()
    st.markdown("### 🖖 Status: **Ready**")

# --- MAIN INTERFACE: CONFIGURATION ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Content Personalization")
    subject = st.text_input("Email Subject", value=EMAIL_SUBJECT)
    body = st.text_area("Email Body (Plain Text)", value=EMAIL_BODY_TEXT, height=350)
    
    st.caption("Available Placeholders: `{company}`, `{sender_name}`")

with col2:
    st.subheader("👥 Target Database")
    uploaded_file = st.file_uploader("Upload your contacts.csv", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(df)} contacts successfully!")
        st.dataframe(df, use_container_width=True, height=250)
        
        # Save locally for the runner logic
        df.to_csv("data/contacts.csv", index=False)
    else:
        st.warning("Please upload a CSV file with 'company' and 'email' columns.")

# --- CAMPAIGN EXECUTION ---
st.divider()

if st.button("🚀 LAUNCH CAMPAIGN"):
    if not email_user or not email_pass:
        st.error("❌ Error: Please provide your SMTP credentials in the sidebar.")
    elif not uploaded_file:
        st.error("❌ Error: No contact list detected.")
    else:
        # Set Environment Variables temporarily for the core modules
        os.environ["SENDER_EMAIL"] = email_user
        os.environ["APP_PASSWORD"] = email_pass
        
        # UI Container for real-time logs
        status_container = st.container()
        
        with st.status("Initializing Engine...", expanded=True) as status:
            # Call the updated runner logic
            run_campaign(status_container)
            status.update(label="Campaign Finished!", state="complete", expanded=False)
        
        st.balloons()
        st.success("🖖 Live Long and Prosper. All emails processed!")

# --- DASHBOARD: POST-CAMPAIGN ANALYTICS ---
if os.path.exists("data/finished.csv"):
    st.divider()
    st.subheader("📊 Last Campaign Analytics")
    finished_df = pd.read_csv("data/finished.csv")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Processed", len(finished_df))
    c2.metric("Success Rate", f"{(len(finished_df[finished_df['status'] == 'SUCCESS']) / len(finished_df) * 100):.1f}%")
    c3.metric("Failures", len(finished_df[finished_df['status'] == 'FAILED']))
