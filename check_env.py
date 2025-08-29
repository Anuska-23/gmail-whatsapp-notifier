import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\anusk\Desktop\Emails_Notifier\email-whatsapp-notifier\.env")

print("TWILIO_SENDER =", os.getenv("TWILIO_SENDER"))
print("WHATSAPP_NUMBER =", os.getenv("WHATSAPP_NUMBER"))
