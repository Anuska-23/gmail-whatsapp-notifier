import imaplib, os
from dotenv import load_dotenv

# Load your .env
load_dotenv(r"C:\Users\anusk\Desktop\Emails_Notifier\email-whatsapp-notifier\.env")

# Connect to Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com")

try:
    mail.login(os.getenv("GMAIL_USERNAME"), os.getenv("GMAIL_APP_PASSWORD"))
    print("✅ Logged in successfully!")
except imaplib.IMAP4.error as e:
    print("❌ Login failed:", e)

mail.logout()
