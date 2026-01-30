
📧 Smart & Resilient SMTP Automator
A professional-grade Python automation engine designed for secure, automated, and anti-blocking email campaigns. This project focuses on simulating human behavior to ensure high deliverability rates and protect your sender reputation when reaching out to multiple recipients (e.g., Law Firms, Recruiters, or Leads).
🛡️ Anti-Blocking & Anti-Spam Engineering
Unlike basic scripts that trigger spam filters by sending bursts of data, this engine implements advanced networking patterns to stay under the radar:
 * Intelligent Rate Limiting: Implements randomized delays between sends and a daily cap (e.g., 50 emails/day) to maintain a healthy sender reputation.
 * Exponential Backoff with Jitter: If the SMTP server is busy or a connection flickers, the script uses a randomized retry strategy to prevent "Thundering Herd" problems.
 * Human-Like Pacing: Variable wait times prevent bot-detection algorithms from flagging the account as an automated spammer.
 * Environment Security: Utilizes .env files and os.getenv to ensure sensitive credentials (Google App Passwords) are never hardcoded or leaked.
🚀 Technical Highlights
 * Atomic Transactions: Contacts are only moved to the "finished" database after a confirmed SMTP "250 OK" status, preventing data loss or duplicate sends.
 * Modular Architecture: Clean separation of concerns between SMTP networking, HTML template rendering, and CSV database management.
 * Robust Error Handling: Integrated logging system that monitors every step, from authentication to final delivery.
🛠️ Project Structure
smtp_email_sender/
├── core/       # Core engine (SMTP logic, Rate Limiting, Retries)
├── config/     # Configuration (Paths, SMTP settings, Daily Limits)
├── data/       # CSV Databases (Pending and Finished contacts)
├── templates/  # Personalizable HTML and Plain Text templates
├── utils/      # Logging and auxiliary system tools
└── runner.py   # Main campaign orchestrator

⚙️ Setup & Installation
 * Clone & Install:
   git clone https://github.com/RicsonRamos/smtp_email_sender.git
cd smtp_email_sender
pip install -r requirements.txt

 * Environment Variables: Create a .env file with your SENDER_EMAIL and APP_PASSWORD.
 * Data Preparation: Add your target list to data/contacts.csv.
 * Execution:
   python runner.py

⚖️ Ethical Usage

This system was built for legitimate, personalized communication. The integration of Rate Limiting and Jitter ensures the integrity of your account while respecting global email delivery standards.

Developed by Ricson  Ramos| ⚖️ Resilience-Driven Automation for Data-Centric Software.

