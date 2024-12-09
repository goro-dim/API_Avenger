import requests

# Test the login endpoint
login_payload = {"username": "user", "password": "pass"}
response = requests.post("http://127.0.0.1:5000/login", json=login_payload)
print("Login Response:", response.json())

# Test the data endpoint
response = requests.get("http://127.0.0.1:5000/data")
print("Data Response:", response.json())
