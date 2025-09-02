from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM = os.getenv("WHATSAPP_FROM")
WHATSAPP_TO = os.getenv("WHATSAPP_TO")

# Check if env variables are loaded
print("TWILIO_SID:", TWILIO_SID)
print("TWILIO_AUTH_TOKEN:", "Loaded" if TWILIO_AUTH_TOKEN else None)
print("WHATSAPP_FROM:", WHATSAPP_FROM)
print("WHATSAPP_TO:", WHATSAPP_TO)

if not all([TWILIO_SID, TWILIO_AUTH_TOKEN, WHATSAPP_FROM, WHATSAPP_TO]):
    raise ValueError("Environment variables missing. Check your .env file!")

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

try:
    message = client.messages.create(
        body="Hello! This is a test message from Twilio WhatsApp.",
        from_=WHATSAPP_FROM,
        to=WHATSAPP_TO
    )
    print("Message sent successfully! SID:", message.sid)
except Exception as e:
    print("Error sending message:", e)
