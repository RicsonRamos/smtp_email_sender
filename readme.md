```markdown
# 📧 Smart & Resilient SMTP Automator

A professional-grade Python automation engine designed for **secure**, **automated**, and **anti-blocking** email campaigns. This project features a modern **Streamlit Dashboard** for real-time management and is fully **Dockerized** for consistent deployment.

It focuses on simulating human behavior to ensure high deliverability rates when reaching out to multiple recipients (e.g., Law Firms, Recruiters, or Leads).

---

## 🛡️ Anti-Blocking & Anti-Spam Engineering

Unlike basic scripts that trigger spam filters, this engine implements advanced patterns to protect your sender reputation:

* **Intelligent Rate Limiting:** Randomized delays between sends to mimic human pacing.
* **Resilient Execution:** Automated retry mechanism with intelligent error handling.
* **Dynamic Personalization:** Injects recipient data (like Company Name) into subjects and bodies in real-time.
* **Session Security:** Credentials are handled via environment variables, never hardcoded.

---

## 🔐 Google App Password Setup

To use this script with Gmail, you **must** use an **App Password**:

1.  **Enable 2FA:** Turn on 2-Step Verification in your [Google Security Settings](https://myaccount.google.com/security).
2.  **Generate Password:** Search for "App Passwords", select "Mail", and name it (e.g., "SMTP Automator").
3.  **Secure the Code:** Save the 16-character code. You will paste it into the App Sidebar.

---

## ⚙️ Quick Start

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone [https://github.com/RicsonRamos/smtp_email_sender.git](https://github.com/RicsonRamos/smtp_email_sender.git)
cd smtp_email_sender
pip install -r requirements.txt

```

### 2. Launching the Dashboard

The easiest way to use the automator is through the Web UI:

```bash
streamlit run app.py

```

### 3. Docker Deployment (Optional)

To run the application in a containerized environment:

```bash
# Build the image
docker build -t smtp-automator .

# Run with persistent volumes (keeps your settings saved)
docker run -p 8501:8501 \
  -v ${PWD}/config:/app/config \
  -v ${PWD}/email.txt:/app/email.txt \
  -v ${PWD}/data:/app/data \
  smtp-automator

```

---

## 📝 Personalization Guide

### 📂 Preparing Contacts

Update `data/contacts.csv` with your targets:

```csv
company,email
Law Firm A,contact@firm-a.com
Global Partners,hr@global-partners.com

```

### 📝 Editing the Template

You can edit the message directly in the **Dashboard** or modify `config/content.py`.

* Use `{company}` to insert the recipient's firm name.
* Use `{sender_name}` to insert your name.

### 📎 Attachments

Simply upload your PDF or DOCX files through the Dashboard. They will be stored in the `attachments/` folder and sent with every email in the campaign.

---

## 🛠️ Project Structure

```text
smtp_email_sender/
├── core/           # SMTP logic and Rate Limiting engine
├── config/         # Configuration files (Subject, Sender Name)
├── data/           # CSV Databases (Contacts and History)
├── attachments/    # Files to be sent as attachments
├── app.py          # Streamlit Web Dashboard (Main Entry)
├── runner.py       # Orchestrator for the mailing process
└── email.txt       # Plain text email body template

```

---

## 📊 Post-Campaign Intelligence

The dashboard includes an **Analytics** section that reads `data/finished.csv` to show:

* Total emails processed.
* Success vs. Failure rates.
* Detailed logs of each transmission.

---

## ⚖️ Ethical Usage

This system was built for legitimate, personalized communication. Please use it responsibly and follow anti-spam regulations (CAN-SPAM, GDPR).

**Developed by Ricson Ramos** | 🖖 *Live long and prosper through automation.*

```
