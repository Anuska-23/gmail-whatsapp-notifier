<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import imaplib
import email
from email.header import decode_header
import time
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# --- Gmail & Twilio Settings ---
EMAIL_ACCOUNT = None
APP_PASSWORD = None
TWILIO_SID = None
TWILIO_AUTH_TOKEN = None
WHATSAPP_SENDER = None
WHATSAPP_RECEIVER = None

# Store emails to avoid duplicates
seen_emails = set()

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    global EMAIL_ACCOUNT, APP_PASSWORD, TWILIO_SID, TWILIO_AUTH_TOKEN, WHATSAPP_SENDER, WHATSAPP_RECEIVER
    
    # Read form data safely
    EMAIL_ACCOUNT = request.form.get('email')
    APP_PASSWORD = request.form.get('app_password')
    TWILIO_SID = request.form.get('sid')
    TWILIO_AUTH_TOKEN = request.form.get('token')
    WHATSAPP_SENDER = request.form.get('sender')
    WHATSAPP_RECEIVER = request.form.get('whatsapp')

    if not all([EMAIL_ACCOUNT, APP_PASSWORD, TWILIO_SID, TWILIO_AUTH_TOKEN, WHATSAPP_SENDER, WHATSAPP_RECEIVER]):
        flash("All fields are required!", "error")
        return redirect(url_for('index'))
    
    return render_template('success.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/new_emails')
def new_emails():
    emails_list = []
    if not EMAIL_ACCOUNT or not APP_PASSWORD:
        return jsonify(emails_list)

    try:
        # Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')
        if status != 'OK':
            return jsonify(emails_list)

        mail_ids = messages[0].split()
        for num in reversed(mail_ids[-10:]):  # get last 10 unread emails
            status, data = mail.fetch(num, '(RFC822)')
            if status != 'OK':
                continue

            msg = email.message_from_bytes(data[0][1])
            
            # Decode email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            
            sender = msg.get("From")
            
            # Avoid duplicates
            unique_id = f"{sender}-{subject}"
            if unique_id in seen_emails:
                continue
            seen_emails.add(unique_id)

            emails_list.append({"sender": sender, "subject": subject})
            
            # --- Send WhatsApp via Twilio ---
            try:
                client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f"New Email from {sender}\nSubject: {subject}",
                    from_=WHATSAPP_SENDER,
                    to=WHATSAPP_RECEIVER
                )
            except Exception as e:
                print(f"Twilio error: {e}")

        mail.logout()

    except imaplib.IMAP4.error as e:
        print(f"Error fetching emails: {e}")

    return jsonify(emails_list)

# --- Run Flask App ---
if __name__ == "__main__":
    app.run(debug=True)
=======
# app.py
from threading import Thread
from notifier.run_web import start_dashboard  # Your dashboard server
from notifier.run_watcher import start_watcher  # Your Gmail watcher

def run_dashboard():
    start_dashboard()  # Starts Flask or any web framework server

def run_watcher():
    start_watcher()  # Checks Gmail and sends WhatsApp messages

if __name__ == "__main__":
    # Run dashboard and watcher concurrently
    t1 = Thread(target=run_dashboard)
    t2 = Thread(target=run_watcher)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
>>>>>>> f080cef47b7602b0f75a02a97606ec338af84d50
