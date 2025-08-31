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
