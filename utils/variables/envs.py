import os
import ipdb

# from emergency_envs import sharepoint_for_database_and_upload_url, sharepoint_medicoes_url
from dotenv import load_dotenv

load_dotenv()

# Keys for login:
username = os.getenv("EMAIL_HOST_USER") # email!
password = os.getenv("EMAIL_HOST_PASSWORD")
nfe_email = os.getenv("EMAIL_NFE")

# Input ids:
hover_selector = os.getenv("HOVER_SELECTOR")
download_selector = os.getenv("DOWNLOAD_SELECTOR")

host_email = os.getenv("EMAIL_HOST_USER")
download_directory = os.getenv("DOWNLOAD_DIRECTORY")
raw_table_directory = os.getenv("RAW_TABLE_DIRECTORY")

# IT IS IMPORTED INCOMPLETE!
# sharepoint_for_database_and_upload_url = os.getenv("SHAREPOINT_FATURAMENTO_URL")
# sharepoint_medicoes_url = os.getenv("SHAREPOINT_MEDICOES_URL")

sharepoint_for_database_and_upload_url="https://jcgestaoderiscos.sharepoint.com/sites/Faturamento/Documentos%20Compartilhados/Forms/AllItems.aspx?e=5%3Ad0583af8e93641b899b91c112ad9763d&at=9&CT=1709221021468&OR=OWA%2DNT%2DMail&CID=8b6264f9%2D36d2%2D1fe7%2Da984%2D3baf620a5479&FolderCTID=0x0120008443E05E6578BA43827BF1DAA2C69915&id=%2Fsites%2FFaturamento%2FDocumentos%20Compartilhados%2F02%20%2D%20FATURAMENTO&viewid=0527a927%2Dcbe6%2D4c31%2D9f6e%2D3133d24b28d3"
sharepoint_medicoes_url="https://jcgestaoderiscos.sharepoint.com/sites/Faturamento/Documentos%20Compartilhados/Forms/AllItems.aspx?id=%2Fsites%2FFaturamento%2FDocumentos%20Compartilhados%2F01%20%2D%20MEDI%C3%87%C3%95ES%2FANO%202024&p=true&fromShare=true&ga=1"
# print("sharepoint_for_database_and_upload_url:", sharepoint_for_database_and_upload_url)
# print("sharepoint_medicoes_url:", sharepoint_medicoes_url)

# Table sheets:
sheet = os.getenv("SHEET")
sheet_contacts = os.getenv("SHEET_CONTACTS")
