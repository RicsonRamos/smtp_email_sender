import streamlit as st
import pandas as pd
import os
from runner import run_campaign
from config.content import SENDER_NAME, EMAIL_SUBJECT

# Configuração da Página
st.set_page_config(page_title="Spock's Mailer", page_icon="🖖", layout="wide")

st.title("📧 Resilient SMTP Automator")
st.markdown(f"**Welcome back, {SENDER_NAME}!** Prepare your campaign below.")

# --- SIDEBAR: Configurações ---
with st.sidebar:
    st.header("⚙️ Configuration")
    sender_email = st.text_input("Your Email", placeholder="email@gmail.com")
    app_password = st.text_input("App Password", type="password")
    
    st.divider()
    st.info("Ensure your 16-digit App Password is ready.")

# --- MAIN: Interface de Usuário ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Message Personalization")
    subject = st.text_input("Email Subject", value=EMAIL_SUBJECT)
    message_body = st.text_area("Message Body", height=300, 
                                help="Use {company} and {sender_name} as placeholders.")

with col2:
    st.subheader("👥 Target List")
    uploaded_file = st.file_file("Upload contacts.csv", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)
        # Salva o arquivo temporariamente para o core processar
        df.to_csv("data/contacts.csv", index=False)
    else:
        st.warning("Please upload a CSV file to begin.")

# --- EXECUTION ---
st.divider()

if st.button("🚀 Start Campaign", use_container_width=True):
    if not sender_email or not app_password:
        st.error("Please provide credentials in the sidebar.")
    elif not uploaded_file:
        st.error("No contacts loaded.")
    else:
        # Atualiza as variáveis de ambiente em tempo de execução
        os.environ["SENDER_EMAIL"] = sender_email
        os.environ["APP_PASSWORD"] = app_password
        
        with st.status("Sending emails...", expanded=True) as status:
            # Aqui chamamos a sua função original de campanha
            # Nota: Você pode precisar adaptar o run_campaign para retornar logs para o Streamlit
            run_campaign() 
            status.update(label="Campaign Finished!", state="complete", expanded=False)
            st.success("All emails processed successfully! 🖖")
