from twilio.rest import Client

def send_whatsapp_message(to_number, message, sid, token, sender):
    try:
        client = Client(sid, token)
        msg = client.messages.create(
            body=message,
            from_=sender,  # e.g. "whatsapp:+14155238886"
            to="whatsapp:" + to_number
        )
        print(f"✅ WhatsApp sent to {to_number}: {message}")
    except Exception as e:
        print("❌ Error sending WhatsApp:", e)
