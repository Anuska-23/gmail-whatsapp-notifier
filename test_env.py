# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()
print("TWILIO_SID:", os.getenv("TWILIO_SID"))
print("TWILIO_AUTH_TOKEN:", os.getenv("TWILIO_AUTH_TOKEN"))
print("WHATSAPP_FROM:", os.getenv("TWILIO_WHATSAPP_FROM"))
print("TO_WHATSAPP_NUMBER:", os.getenv("TO_WHATSAPP_NUMBER"))
