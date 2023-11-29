import os

from shareplum import Site, Office365
from shareplum.site import Version

from dotenv import load_dotenv

import ipdb

load_dotenv()

# machine_path = os.getcwd()

# machine_path = "C:\Users\andre.kuratomi\"
machine_path = os.environ.get("MACHINE_URL")
site_url = os.environ.get("SHAREPOINT_URL")
folder_path = os.environ.get("SHAREPOINT_PATH")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

def connect_sharepoint(username, password, sharepoint_url):
    authentication = Office365(sharepoint_url, username=username, password=password).get_cookies()
    if authentication:  
        return Site(sharepoint_url, version=Version.v365, auth=authentication)
    else:
        return None

sp = connect_sharepoint(username, password, site_url)

folder = sp.folder(machine_path + folder_path)
ipdb.set_trace()

# table_name = "your_table_name"
# table = folder.get_list(table_name)

# directory_path = 
# folder = site.Folder(directory_path)
  
# files = folder.files
# for file in files:
#     print(file['Name'])
