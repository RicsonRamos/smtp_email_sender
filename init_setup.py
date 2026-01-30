import os
from utils.helpers import ensure_directory

def initialize_project():
    """
    Automates the initial environment setup for the SMTP sender.
    """
    print("🖖 Initializing Spock's SMTP Automator Setup...")

    # 1. Create necessary directories
    directories = ["data", "logs", "attachments", "templates", "config", "core", "utils"]
    for folder in directories:
        ensure_directory(folder)
        print(f"✅ Directory check: {folder}/")

    # 2. Create a template .env file if it doesn't exist
    if not os.path.exists(".env"):
        with open(".env", "w", encoding="utf-8") as f:
            f.write("SENDER_EMAIL=your-email@gmail.com\n")
            f.write("APP_PASSWORD=xxxx-xxxx-xxxx-xxxx\n")
        print("✅ Created .env template. Please add your credentials.")
    else:
        print("ℹ️  .env file already exists. Skipping.")

    # 3. Create a sample contacts.csv if it doesn't exist
    csv_path = "data/contacts.csv"
    if not os.path.exists(csv_path):
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("company,email\n")
            f.write("Example Firm,hr@example.com\n")
        print(f"✅ Created sample database at {csv_path}")

    # 4. Final instructions
    print("\n🚀 Setup Complete!")
    print("-" * 30)
    print("Next steps:")
    print("1. Fill your .env with your Google App Password.")
    print("2. Add your attachments to the 'attachments/' folder.")
    print("3. Run 'python main.py' to start your campaign.")
    print("-" * 30)

if __name__ == "__main__":
    initialize_project()
