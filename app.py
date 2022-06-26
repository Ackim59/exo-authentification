from App import app
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(override=True)
    app.run(host="0.0.0.0", port=8000, debug=app.config['DEBUG'])