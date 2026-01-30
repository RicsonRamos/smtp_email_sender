
# 📧 Smart & Resilient SMTP Automator

A professional-grade Python automation engine designed for **secure**, **automated**, and **anti-blocking** email campaigns. This project focuses on simulating human behavior to ensure high deliverability rates and protect your sender reputation when reaching out to multiple recipients (e.g., Law Firms, Recruiters, or Leads).

## 🛡️ Anti-Blocking & Anti-Spam Engineering

Unlike basic scripts that trigger spam filters by sending bursts of data, this engine implements advanced networking patterns to stay under the radar:

* **Intelligent Rate Limiting:** Implements randomized delays between sends and a daily cap (e.g., 50 emails/day).
* **Exponential Backoff with Jitter:** Uses a randomized retry strategy if the connection fails.
* **Human-Like Pacing:** Variable wait times prevent bot-detection algorithms from flagging the account.
* **Environment Security:** Credentials are kept safe in a `.env` file, never hardcoded.



## 🔐 Security: Google App Password Setup

To use this script with Gmail, you **must** use an **App Password**.

1.  **Enable 2FA:** Ensure **2-Step Verification** is ON in your [Google Security Settings](https://myaccount.google.com/security).
2.  **Generate App Password:** Search for "App Passwords" in your Google Account.
3.  **Name it:** Call it "Python Email" and click **Create**.
4.  **Copy & Save:** Save the 16-character code. You will paste it into the `.env` file.



## ⚙️ Setup & Installation

1.  **Clone & Install:**
    ```bash
    git clone [https://github.com/RicsonRamos/smtp_email_sender.git](https://github.com/RicsonRamos/smtp_email_sender.git)
    cd smtp_email_sender
    pip install -r requirements.txt
    ```

2.  **Environment Variables:** Create a file named `.env` in the root folder:
    ```text
    SENDER_EMAIL=your-email@gmail.com
    APP_PASSWORD=xxxx-xxxx-xxxx-xxxx  # Your 16-digit Google App Password
    ```

## 📝 Customization Guide (How to Personalize)

You can easily customize who receives the emails and what the message says without touching the core logic.

### 1. Preparing your Contacts
Open the file `data/contacts.csv`. This is your database. Fill it using this format:
```csv
company,email
Law Firm A,contact@firm-a.com
Global Partners,hr@global-partners.com

 * company: The name of the firm (used to personalize the email).
 * email: The recipient's address.
2. Customizing the Message
Go to config/content.py. This file controls the subject and the text:
 * Change EMAIL_SUBJECT to your desired title.
 * Edit EMAIL_BODY_TEXT to write your letter.
 * Important: Keep the tags {company} and {sender_name} where you want the script to automatically insert the firm's name and your name (Spock).
3. Visual Template (Optional)
If you want to change the visual look (colors/layout), edit templates/generic_template.html. The script will automatically wrap your text into this professional design.
🚀 Execution
Once your contacts are in the CSV and your message is set in content.py, simply run:
python runner.py

The script will:
 * Read each contact.
 * Wait for a random, safe interval.
 * Send the personalized email with your resume attached.
 * Move the contact to finished.csv once successful.
🛠️ Project Structure
smtp_email_sender/
├── core/       # Core engine (SMTP logic, Rate Limiting)
├── config/     # Message and Subject configuration
├── data/       # CSV Databases (Contacts list)
├── templates/  # HTML and Plain Text visual templates
├── utils/      # Helper tools (Text cleaning, logs)
└── runner.py   # Main orchestrator (Run this file)

⚖️ Ethical Usage
This system was built for legitimate, personalized communication. Please use it responsibly.
Developed by Spock | ⚖️ Resilience-Driven Automation for Data-Centric Software.
