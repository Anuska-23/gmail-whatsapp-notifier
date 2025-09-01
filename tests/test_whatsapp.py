from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load .env
load_dotenv(r"C:\Users\anusk\Desktop\Emails_Notifier\email-whatsapp-notifier\.env")

# Twilio client
client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))

# Send test message
message = client.messages.create(
    body="✅ Hello! This is a test WhatsApp message from your notifier.",
    from_=os.getenv("TWILIO_SENDER"),
    to=os.getenv("WHATSAPP_NUMBER")
)

print("Message SID:", message.sid)
