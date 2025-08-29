from web.app import create_app
from notifier.config import WEB_HOST, WEB_PORT

if __name__ == "__main__":
    app = create_app()
    app.run(host=WEB_HOST, port=WEB_PORT, debug=False)
