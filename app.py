from App import create_app
from dotenv import load_dotenv
from config import config
import os

load_dotenv(override=True)
config_name = os.getenv("FLASK_CONFIG")

if __name__ == "__main__":
    app = create_app(config_name)
    if os.getenv('FLASK_CONFIG') == "development":
        app.run(debug=app.config['DEBUG'])
    elif os.getenv('FLASK_CONFIG') == "production":
        app.run(debug=app.config['DEBUG'])
    elif os.getenv('FLASK_CONFIG') == "azure":
        app.run(host="0.0.0.0", port=8000, debug=app.config['DEBUG'])