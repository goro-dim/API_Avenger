import json

def create_config():
    secret_key = input("Enter your secret key: ")
    config = {
        "SECRET_KEY": secret_key
    }
    with open("config.json", 'w') as config_file:
        json.dump(config, config_file, indent=4)
    print("Configuration file created. Please make sure to keep it secure.")

if __name__ == "__main__":
    create_config()
