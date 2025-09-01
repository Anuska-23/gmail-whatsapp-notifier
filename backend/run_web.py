<<<<<<< HEAD
from web.app import create_app
from notifier.config import WEB_HOST, WEB_PORT

if __name__ == "__main__":
    app = create_app()
    app.run(host=WEB_HOST, port=WEB_PORT, debug=False)
=======
from flask import Flask

def start_dashboard():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Dashboard running!"

    app.run(debug=True, port=5000)

>>>>>>> f080cef47b7602b0f75a02a97606ec338af84d50
