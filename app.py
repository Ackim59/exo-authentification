from App import app
from dotenv import load_dotenv
from config import config
import os

if __name__ == "__main__":
    load_dotenv(override=True)
    if os.getenv('FLASK_CONFIG') == "development":
        app.run(debug=app.config['DEBUG'])
    elif os.getenv('FLASK_CONFIG') == "production":
        app.run(debug=app.config['DEBUG'])#
    elif os.getenv('FLASK_CONFIG') == "azure":
        app.run(host="0.0.0.0", port=8000, debug=app.config['DEBUG'])#