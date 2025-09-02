import os
import pickle
import time
import schedule
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from twilio.rest import Client
from dotenv import load_dotenv
import googleapiclient.discovery

print("Running email_to_whatsapp.py...")

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
# Load .env
load_dotenv()
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
TO_WHATSAPP_NUMBER = os.getenv("TO_WHATSAPP_NUMBER")

# Check Twilio credentials
if not all([TWILIO_SID, TWILIO_AUTH_TOKEN, WHATSAPP_FROM, TO_WHATSAPP_NUMBER]):
    raise ValueError("Twilio credentials missing or incorrect in .env file!")

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp(to, message):
    client.messages.create(
        from_=WHATSAPP_FROM,
        body=message,
        to=f"whatsapp:{to.replace('whatsapp:', '')}"
    )

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)
    return service

def check_email():
    service = get_gmail_service()

    results = service.users().messages().list(
        userId='me', labelIds=['INBOX'], q="is:unread"
    ).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No new emails.")
    else:
        for msg in messages:
            message = service.users().messages().get(
                userId='me', id=msg['id']
            ).execute()
            payload = message['payload']
            headers = payload.get("headers", [])
            subject = ""
            from_email = ""
            for header in headers:
                if header['name'] == 'From':
                    from_email = header['value']
                if header['name'] == 'Subject':
                    subject = header['value']
            body = f"New Email from {from_email}\nSubject: {subject}"
            send_whatsapp(TO_WHATSAPP_NUMBER, body)
            # Mark message as read
            service.users().messages().modify(
                userId='me',
                id=msg['id'],
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            print(f"Sent WhatsApp alert for: {subject}")

# Schedule to check email every minute
schedule.every(1).minutes.do(check_email)

print("Email to WhatsApp notifier is running...")
while True:
    schedule.run_pending()
    time.sleep(1)

