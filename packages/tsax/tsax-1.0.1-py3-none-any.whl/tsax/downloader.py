import getpass
import requests
import os

def download_file():
    CORRECT_PASSCODE = "2346" 
    FILE_URL = "https://drive.google.com/uc?export=download&id=1vX30HNpPwCk6NcB9mE36blfsbo7ifRW4"
    FILE_NAME = "TSAX.zip"

    print("Welcome to X-Chamber !!")
    passcode = getpass.getpass("Enter the passcode: ")

    if passcode == CORRECT_PASSCODE:
        try:
            print("Downloading the file...")
            response = requests.get(FILE_URL, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", FILE_NAME)

            with open(desktop_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"File downloaded successfully to {desktop_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the file: {e}")
    else:
        print("Incorrect passcode. Access denied.")
