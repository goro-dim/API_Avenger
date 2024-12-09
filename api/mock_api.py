from flask import Flask, request, jsonify
import logging
import jwt
import datetime
import os
import json

app = Flask(__name__)

# Secret key for JWT signing (read from a JSON config file or environment variable)
SECRET_KEY = None

# Load secret key from config.json
CONFIG_FILE = "config.json"

try:
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        SECRET_KEY = config.get("SECRET_KEY")
except FileNotFoundError:
    print(f"[!] {CONFIG_FILE} not found. Falling back to environment variable.")
except json.JSONDecodeError:
    raise RuntimeError(f"[!] {CONFIG_FILE} is not valid JSON. Please check its contents.")

# Fallback to environment variable if JSON config fails
if not SECRET_KEY:
    SECRET_KEY = os.environ.get("SECRET_KEY")

# Raise an error if SECRET_KEY is still not set
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not set. Please provide it in a config.json file or set it as an environment variable."
    )

# Set up logging
logging.basicConfig(
    filename="api_requests.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

# Mock database of credentials
VALID_CREDENTIALS = {
    "admin": "admin123",
    "user": "pass123",
    "guest": "guest123",
}

@app.before_request
def log_request_info():
    # Log incoming request data
    log_data = {
        "path": request.path,
        "method": request.method,
        "ip": request.remote_addr,
        "data": request.get_data(as_text=True),
        "content_length": request.content_length,
    }
    app.logger.info(log_data)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to API Avenger! Use /login, /token, or /data for interaction."})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Invalid input"}), 400

    username = data["username"]
    password = data["password"]

    if VALID_CREDENTIALS.get(username) == password:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/token', methods=['POST'])
def get_token():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Invalid input"}), 400

    username = data["username"]
    password = data["password"]

    if VALID_CREDENTIALS.get(username) == password:
        # Create JWT token with timezone-aware UTC time
        token = jwt.encode(
            {
                "username": username,
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        # Decode token to UTF-8 if needed
        token = token.decode('utf-8') if isinstance(token, bytes) else token
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/data', methods=['GET'])
def get_data():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing token"}), 401

    try:
        # Extract token from header
        token = auth_header.split(" ")[1]
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"data": "Sensitive information"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == '__main__':
    app.run(debug=True)
