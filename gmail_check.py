import imaplib
import email
from email.header import decode_header
import os
import time
from dotenv import load_dotenv
from notifier.whatsapp import send_whatsapp_message

# Load environment variables
load_dotenv(r"C:\Users\anusk\Desktop\Emails_Notifier\email-whatsapp-notifier\.env")

def start_watching():
    print("📬 Gmail watcher started! Waiting for new emails...")

    # Connect to Gmail
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(os.getenv("GMAIL_USERNAME"), os.getenv("GMAIL_APP_PASSWORD"))
        mail.select("inbox")
    except Exception as e:
        print("❌ Error connecting to Gmail:", e)
        return

    # Initialize seen emails (so existing emails are ignored)
    try:
        result, data = mail.uid('search', None, "ALL")
        if result != 'OK':
            print("❌ Error fetching initial emails")
            seen_uids = set()
        else:
            seen_uids = set(data[0].split())
    except Exception as e:
        print("❌ Error initializing seen emails:", e)
        seen_uids = set()

    # Start checking for new emails continuously
    while True:
        try:
            result, data = mail.uid('search', None, "ALL")
            if result != 'OK':
                print("❌ Error searching emails")
                time.sleep(15)
                continue

            uids = data[0].split()
            new_uids = [uid for uid in uids if uid not in seen_uids]

            for uid in new_uids:
                result, msg_data = mail.uid('fetch', uid, '(RFC822)')
                if result != 'OK':
                    print(f"❌ Failed to fetch email UID {uid.decode()}")
                    continue

                raw_email_bytes = msg_data[0][1]
                msg = email.message_from_bytes(raw_email_bytes)

                # Decode subject
                subject, encoding = decode_header(msg.get("Subject"))[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                # From address
                sender = msg.get("From")

                # Print new email info in terminal
                print(f"📧 New email from: {sender} | Subject: {subject}")

                # Send WhatsApp alert
                try:
                    send_whatsapp_message(f"📧 New email from: {sender}\nSubject: {subject}")
                except Exception as e:
                    print("❌ Error sending WhatsApp message:", e)

                # Mark UID as seen
                seen_uids.add(uid)

            # Wait before next check
            time.sleep(15)

        except Exception as e:
            print("❌ Error during email checking:", e)
            time.sleep(15)

# Run watcher
if __name__ == "__main__":
    start_watching()
