import os

from dotenv import load_dotenv

load_dotenv()

# Keys for login:
username = os.getenv("USERN")
password = os.getenv("PASSWORD")

# Input ids:
hover_selector = os.getenv("HOVER_SELECTOR")
download_selector = os.getenv("DOWNLOAD_SELECTOR")

host_email = os.getenv("EMAIL_HOST_USER")
download_directory = os.getenv("DOWNLOAD_DIRECTORY")
sharepoint_url = os.getenv("SHAREPOINT_URL")