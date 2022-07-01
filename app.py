from App import app
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(override=True)
    app.run(debug=app.config['DEBUG'])#host="0.0.0.0", port=8000, 