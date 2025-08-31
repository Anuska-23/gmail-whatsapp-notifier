from twilio.rest import Client
import os

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp(to, message):
    to_number = f"whatsapp:{to}"
    client.messages.create(
        body=message,
        from_=WHATSAPP_FROM,
        to=to_number
    )
