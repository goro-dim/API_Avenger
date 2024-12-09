import requests
import json

# Mock API endpoints
BASE_URL = "http://127.0.0.1:5000"
TOKEN_ENDPOINT = f"{BASE_URL}/token"
DATA_ENDPOINT = f"{BASE_URL}/data"

# Credentials to fetch a valid token
VALID_CREDENTIALS = {
    "username": "admin",
    "password": "admin123"
}

# Simulated stolen token (empty initially)
stolen_token = None

def check_server_status():
    """
    Check if the mock API server is running and configured correctly.
    """
    print("[*] Checking server status...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print(f"[+] Server is running. Response: {response.json().get('message')}")
        else:
            print(f"[-] Unexpected server response. Status: {response.status_code}, Response: {response.text}")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("[-] Unable to connect to the server. Is it running?")
        exit(1)

def fetch_valid_token():
    """
    Fetch a valid JWT from the /token endpoint using predefined credentials.
    """
    global stolen_token
    print("[*] Fetching a valid token...")
    response = requests.post(TOKEN_ENDPOINT, json=VALID_CREDENTIALS)
    if response.status_code == 200:
        stolen_token = response.json().get("token")
        if not stolen_token:
            print("[-] Failed to retrieve a valid token. No token returned by the server.")
            exit(1)
        print(f"[+] Successfully obtained token: {stolen_token}")
    else:
        print(f"[-] Failed to fetch token. Status: {response.status_code}, Response: {response.text}")
        exit(1)

def replay_token():
    """
    Replay the stolen token to access the /data endpoint.
    """
    if not stolen_token:
        print("[-] No token available to replay. Fetch a valid token first.")
        return

    print("[*] Replaying the stolen token...")
    headers = {"Authorization": f"Bearer {stolen_token}"}
    response = requests.get(DATA_ENDPOINT, headers=headers)

    if response.status_code == 200:
        print(f"[+] Replay successful! Data: {response.json().get('data')}")
    elif response.status_code == 401:
        print(f"[-] Replay failed. Unauthorized access. Response: {response.text}")
    else:
        print(f"[-] Unexpected response. Status: {response.status_code}, Response: {response.text}")

def simulate_expired_token():
    """
    Simulate the use of an expired token.
    """
    if not stolen_token:
        print("[-] No token available to simulate expiration. Fetch a valid token first.")
        return

    print("[*] Simulating expired token...")
    # Tamper with the stolen token to simulate expiration or invalid signature
    expired_token = stolen_token[:-5] + "ABCDE"  # Modify the token
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = requests.get(DATA_ENDPOINT, headers=headers)

    if response.status_code == 401:
        print(f"[+] Expired token correctly rejected. Response: {response.text}")
    else:
        print(f"[-] Expired token unexpected behavior. Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    print("=== Token Stealing and Replay Script ===")
    check_server_status()
    fetch_valid_token()
    replay_token()
    simulate_expired_token()
