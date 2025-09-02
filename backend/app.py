import os
import threading
import time
import schedule
import imaplib
import email
from email.header import decode_header
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from twilio.rest import Client

# --- Flask app ---
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")

# --- Global variables ---
EMAIL_ACCOUNT = None
APP_PASSWORD = None
TWILIO_SID = None
TWILIO_AUTH_TOKEN = None
WHATSAPP_SENDER = None
WHATSAPP_RECEIVER = None

seen_emails = set()
emails_list = []  # Store emails for dashboard

# --- Twilio WhatsApp function ---
def send_whatsapp(sender, receiver, body, sid, auth_token):
    try:
        client = Client(sid, auth_token)
        if not sender.startswith("whatsapp:"):
            sender = f"whatsapp:{sender}"
        if not receiver.startswith("whatsapp:"):
            receiver = f"whatsapp:{receiver}"
        message = client.messages.create(
            from_=sender,
            to=receiver,
            body=body
        )
        print(f"WhatsApp sent: SID {message.sid}")
    except Exception as e:
        print(f"Twilio error: {e}")

# --- Fetch emails from Gmail and send WhatsApp ---
def fetch_emails():
    global emails_list
    if not (EMAIL_ACCOUNT and APP_PASSWORD and TWILIO_SID and TWILIO_AUTH_TOKEN):
        return

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')
        if status != 'OK':
            mail.logout()
            return

        mail_ids = messages[0].split()
        for num in reversed(mail_ids[-10:]):  # Last 10 unread emails
            status, data = mail.fetch(num, '(RFC822)')
            if status != 'OK':
                continue

            msg = email.message_from_bytes(data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            sender_email = msg.get("From")
            unique_id = f"{sender_email}-{subject}"

            if unique_id in seen_emails:
                continue
            seen_emails.add(unique_id)
            emails_list.append({"sender": sender_email, "subject": subject})

            # Send WhatsApp
            send_whatsapp(
                sender=WHATSAPP_SENDER,
                receiver=WHATSAPP_RECEIVER,
                body=f"New Email from {sender_email}\nSubject: {subject}",
                sid=TWILIO_SID,
                auth_token=TWILIO_AUTH_TOKEN
            )

        mail.logout()
    except imaplib.IMAP4.error as e:
        print(f"Error fetching emails: {e}")

# --- Scheduler thread ---
def run_scheduler():
    schedule.every(1).minutes.do(fetch_emails)
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler, daemon=True).start()

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    global EMAIL_ACCOUNT, APP_PASSWORD, TWILIO_SID, TWILIO_AUTH_TOKEN, WHATSAPP_SENDER, WHATSAPP_RECEIVER
    
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
    return render_template('dashboard.html', emails=emails_list)

@app.route('/new_emails')
def new_emails():
    return jsonify(emails_list)

# --- Run Flask App ---
if __name__ == "__main__":
    print("Templates folder:", os.path.join(os.path.dirname(__file__), "templates"))
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
