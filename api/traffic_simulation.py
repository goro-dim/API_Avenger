import requests
import time
import random

# Define payloads
usernames = ["admin", "user", "guest", "test"]
passwords = ["admin", "password", "guest", "12345"]

# Base URL
base_url = "http://127.0.0.1:5000"

# Simulate login attempts
for username in usernames:
    for password in passwords:
        payload = {"username": username, "password": password}
        response = requests.post(f"{base_url}/login", json=payload)
        print(f"Attempted login with {username}:{password} - Status Code: {response.status_code}")
        time.sleep(random.uniform(0.5, 2))  # Add a random delay between 0.5 to 2 seconds

# Simulate data access
response = requests.get(f"{base_url}/data")
print("Data access status code:", response.status_code)
