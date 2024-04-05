import os
import ipdb

# from emergency_envs import sharepoint_for_database_and_upload_url, sharepoint_medicoes_url
from dotenv import load_dotenv

load_dotenv()

django_secret = os.getenv("SECRET_KEY").replace('*', '=')

# Keys for login:
user_email = os.getenv("EMAIL_HOST_USER")
password = os.getenv("EMAIL_HOST_PASSWORD")
nfe_email = os.getenv("EMAIL_NFE")

# Input ids:
hover_selector = os.getenv("HOVER_SELECTOR")
download_selector = os.getenv("DOWNLOAD_SELECTOR")

host_email = os.getenv("EMAIL_HOST_USER")
download_directory = os.getenv("DOWNLOAD_DIRECTORY")
raw_table_directory = os.getenv("RAW_TABLE_DIRECTORY")

# IT IS IMPORTED INCOMPLETE! It doens't accept '=' character.
sharepoint_for_database_and_upload_url = os.getenv("SHAREPOINT_FATURAMENTO_URL").replace('*', '=')
sharepoint_medicoes_url = os.getenv("SHAREPOINT_MEDICOES_URL").replace('*', '=')
# ipdb.set_trace()

# Table sheets:
sheet = os.getenv("SHEET")
sheet_contacts = os.getenv("SHEET_CONTACTS")
