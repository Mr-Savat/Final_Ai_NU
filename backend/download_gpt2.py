import os
import requests
import zipfile

GITHUB_RELEASE_URL = "https://github.com/Mr-Savat/NU_Chatbot/releases/download/v1.0-train/gpt2-norton.zip"
DOWNLOAD_PATH = "gpt2-norton.zip"
EXTRACT_PATH = "gpt2-norton"

def download_gpt2():
    if not os.path.exists(EXTRACT_PATH):
        print("[*] Downloading GPT-2 training folder from Release...")
        r = requests.get(GITHUB_RELEASE_URL, stream=True)
        with open(DOWNLOAD_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        print("[*] Extracting zip...")
        with zipfile.ZipFile(DOWNLOAD_PATH, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_PATH)
        os.remove(DOWNLOAD_PATH)
        print("[+] GPT-2 folder ready")
    else:
        print("[*] GPT-2 folder already exists")
