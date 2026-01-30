```markdown
# 📧 Resilient SMTP Email Sender (Law Internship Automation)

A professional-grade Python automation engine designed to send summaries and cover letters to law firms. This project focuses on **resilience**, **security**, and **anti-spam techniques** to ensure high delivery rates and account security.



## 🚀 Key Engineering Features

Unlike simple scripts, this engine implements advanced networking and automation patterns:

* **Exponential Backoff with Jitter:** Prevents "Thundering Herd" problems by randomizing retry times if the SMTP server is busy or the connection flickers.
* **Intelligent Rate Limiting:** Simulates human behavior with randomized delays between emails and a daily cap (e.g., 50 emails/day) to protect your Gmail account from being flagged as spam.
* **Atomic Transactions:** Ensures contacts are only moved to the "finished" list after successful delivery, preventing data loss.
* **Modular Architecture:** Clean separation of concerns between SMTP logic, content building, and contact management.
* **Environment Security:** Sensitive credentials are never hardcoded, utilizing `.env` files and `os.getenv`.

## 🛠️ Project Structure

```text
smtp_email_sender/
├── core/ # Core engine (SMTP, Rate Limit, Retries)
├── config/ # Configuration (Paths, SMTP settings, Limits)
├── data/ # CSV Databases (Pending and Finished contacts)
├── templates/ # HTML and Plain Text email templates
├── utils/ # Logging and auxiliary tools
├── attachments/ # PDF Resume storage
└── main.py # Application entry point

```

## ⚙️ Setup & Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/your-username/smtp_email_sender.git](https://github.com/RicsonRamos/smtp_email_sender.git)
cd smtp_email_sender

```


2. **Create a Virtual Environment:**
```bash
python -m venv .venv
source .venv/bin/activate # Windows: .\.venv\Scripts\activate

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure Environment Variables:**
Create a `.env` file in the root directory:
```text
SENDER_EMAIL=your-email@gmail.com
APP_PASSWORD=your-google-app-password

```


5. **Prepare your Data:**
* Add your contacts to `data/contacts.csv`.
* Place your `resume.pdf` in the `attachments/` folder.



## 📈 Usage

Simply run the main orchestrator:

```bash
python main.py

```

The system will automatically:

1. Load pending contacts.
2. Authenticate securely with Gmail.
3. Build personalized HTML emails for each law firm.
4. Send them respecting the configured rate limits.
5. Log every step and move successful contacts to `finished.csv`.

## 🛡️ Security Note

This project uses **Google App Passwords**. Never use your primary account password. The `.env` file is included in `.gitignore` to prevent accidental credential leaks.

---

Developed by **Spoke** | ⚖️ Focused on Legal Career Automation.

```

---

### 💡 Additional Tips for GitHub:

1. **Screenshot:** Add an image or GIF of the terminal running the script (like that log you sent me). This gives "life" to the project.

2. **`requirements.txt`:** Don't forget to create it. Just run:

```bash
pip freeze > requirements.txt

```
3. **About on GitHub:** On the right side of the repository page, fill in the "About" section with keywords: `Python`, `SMTP`, `Automation`, `Software Engineering`.

**What do you think of this README, Spoke?** Do you want me to add a specific section about how you customized the Criminal Law templates, or are we ready for the final commit?

```