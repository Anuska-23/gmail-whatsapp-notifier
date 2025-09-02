
from .whatsapp import send_whatsapp_message

from notifier.gmail_watcher import GmailWatcher


from notifier.gmail_watcher import GmailWatcher


if __name__ == "__main__":
    GmailWatcher().run_forever()
