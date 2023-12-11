import os
import requests
import shutil
import time

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import ipdb


load_dotenv()

# ENVS:
# Keys for login:
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Input ids:
username_input_id = os.getenv("USER_INPUT_ID")
password_input_id = os.getenv("PASSWORD_INPUT_ID")

# Sharepoint URL:
sharepoint_url = os.getenv("SHAREPOINT_URL")

# Download directory:
download_directory = str(os.getenv("DOWNLOAD_DIRECTORY"))


# def robot_for_sharepoint(username: str, password: str, user_id: str, pass_id: str, share_url: str, download_dir: str):
# CONNECT TO BROWSER:
# Driver instance:
options = webdriver.EdgeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": download_directory,
    # "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    'download.directory_upgrade': True,
    "safebrowsing.enabled": True
})

driver = webdriver.Edge(options=options)

# Navigate to Sharepoint login page and maximize its window:
driver.get(sharepoint_url)
# driver.get(share_url)
driver.maximize_window()

# LOGIN:
# Find username input field by its ID and enter email address:
username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, username_input_id)))
# username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, user_id)))

# Enter password and submit the form:
username_input.send_keys(username)
username_input.send_keys(Keys.RETURN)

# Wait for the password input to be visible:
password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, password_input_id)))
# password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, pass_id)))

# Enter password and submit the form:
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)

# Hovering an element:
item = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-selection-index='1']")))
item.click()

# Create an instance of ActionChains and perform the hover action
actions = ActionChains(driver)
actions.move_to_element(item).perform()

download = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-automationid='downloadCommand']")))
download.click()

    # driver.close()

# robot_for_sharepoint(username, password, username_input_id, password_input_id, sharepoint_url, download_directory)


# download_directory = r"/mnt/c/Users/andre.kuratomi/Projects/vba_python_django/management/commands/raw_table/"
# wrong_download_directory = "C:/Users/andre.kuratomi/Projects/vba_python_django/management/commands/raw_table"
# # Paths:
# path_to_windows_sharepoint = "/mnt/c/Users/andre.kuratomi/JC Gestao de Riscos/Testes Desenvolvimento - Documentos/General"
# path_to_web_driver = "/mnt/c/Users/andre.kuratomi/Downloads/msedgedriver.exe"

# NOW WORK WITH SHAREPOINT'S CONTENT:
# documents = driver.find_element(By.CSS_SELECTOR, "a[class='ms-Nav-link link_4a471f57']")
# documents.click()
# item = driver.find_element(By.CSS_SELECTOR, "div[data-list-index='2']")
# item = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-list-index='2']")))

# # Redirecting for now:
# time.sleep(5)  # wait for file to be created
# old_path = os.path.join(wrong_download_directory, "Monitoramento Can Cariacica 12")
# shutil.move(old_path, download_directory)


# # Find the table element
# table = driver.find_element(By.CSS_SELECTOR, "div[class=ewr-grdcontarea-ltr ewr-grdcontarea-grid customScrollBar ewa-scrollbars-enabled]")

# # Retrieve the table content
# table_content = table.get_attribute("innerHTML")

# # Save the content as a file
# file_path = "/home/andrekuratomi/Projects/vba_python_django/management/commands/raw_table.xlsm"
# with open(file_path, "w", encoding="utf-8") as file:
#     file.write(table_content)


# Get the table HTML content
# table_html = driver.page_source
# # print(table_html)
# # Save the table HTML content to a file
# with open('/home/andrekuratomi/Projects/vba_python_django/management/commands/raw_table/something.xlsm', 'w') as file:
#     file.write(table_html)

# table = driver.find_element(By.CLASS_NAME, "div[class='ewr-grdcontarea-ltr ewr-grdcontarea-grid customScrollBar ewa-scrollbars-enabled']")
# table_html = table.get_attribute("outerHTML")

# file_path = "/home/andrekuratomi/Projects/vba_python_django/management/commands/raw_table/table.html"
# with open(file_path, "w") as file:
#     file.write(table_html)
