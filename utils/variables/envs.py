import os
import ipdb

from emergency_envs import sharepoint_for_database_and_upload_url, sharepoint_medicoes_url
from dotenv import load_dotenv

load_dotenv()

# Keys for login:
username = os.getenv("EMAIL_HOST_USER")
password = os.getenv("EMAIL_HOST_PASSWORD")
# username = os.getenv("PERSONAL_USER")
# password = os.getenv("PERSONAL_PASSWORD")
username_test = os.getenv("EMAIL_HOST_USER_TEST")
password_test = os.getenv("EMAIL_HOST_PASSWORD_TEST")

# Input ids:
hover_selector = os.getenv("HOVER_SELECTOR")
download_selector = os.getenv("DOWNLOAD_SELECTOR")

host_email = os.getenv("EMAIL_HOST_USER")
download_directory = os.getenv("DOWNLOAD_DIRECTORY")
raw_table_directory = os.getenv("RAW_TABLE_DIRECTORY")

# IT IS IMPORTED INCOMPLETE!
# sharepoint_for_database_and_upload_url = os.getenv("SHAREPOINT_FATURAMENTO_URL")
# sharepoint_medicoes_url = os.getenv("SHAREPOINT_MEDICOES_URL")

sharepoint_for_database_and_upload_url = sharepoint_for_database_and_upload_url
sharepoint_medicoes_url = sharepoint_medicoes_url
# print("sharepoint_for_database_and_upload_url:", sharepoint_for_database_and_upload_url)
# print("sharepoint_medicoes_url:", sharepoint_medicoes_url)
# ipdb.set_trace()
sheet = os.getenv("SHEET")
# sharepoint_url = os.getenv("SHAREPOINT_URL")
