<<<<<<< HEAD
from .whatsapp import send_whatsapp_message
=======
from notifier.gmail_watcher import GmailWatcher

>>>>>>> f080cef47b7602b0f75a02a97606ec338af84d50


if __name__ == "__main__":
    GmailWatcher().run_forever()
