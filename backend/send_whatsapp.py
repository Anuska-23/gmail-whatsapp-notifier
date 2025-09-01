from twilio.rest import Client
import os

def send_whatsapp_message(message):
    to_number = os.getenv("WHATSAPP_NUMBER")
    from_number = os.getenv("TWILIO_SENDER")
    
    print("Sending WhatsApp message:")
    print("To:", to_number)
    print("From:", from_number)
    print("Message:", message)
    
    client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
    client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )
