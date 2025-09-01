from flask import Flask

def start_dashboard():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Dashboard running!"

    app.run(debug=True, port=5000)

