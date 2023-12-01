import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import ipdb

# Keys for login:
username = "naoresponda@jcgestaoderiscos.com.br"
password = "Bus84246"

# Paths:
path_to_windows_sharepoint = "/mnt/c/Users/andre.kuratomi/JC Gestao de Riscos/Testes Desenvolvimento - Documentos/General"
path_to_web_driver = "/mnt/c/Users/andre.kuratomi/Downloads/msedgedriver.exe"

# Input ids:
username_input_id = "i0116"
password_input_id = "i0118"

# CONNECT TO BROWSER:
# Driver instance:
options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)

# Navigate to Sharepoint login page:
driver.get("https://jcgestaoderiscos.sharepoint.com/sites/testes.desenvolvimento")
# Print the HTML source

# LOGIN:
# Find username input field by its ID and enter email address:
username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, username_input_id)))

# Enter password and submit the form:
username_input.send_keys(username)
username_input.send_keys(Keys.RETURN)

# Wait for the password input to be visible:
password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, password_input_id)))

# Enter password and submit the form:
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)

# Now work with sharepoint`s content:
# documents = driver.find_element(By.CSS_SELECTOR, "a[class='ms-Nav-link link_4a471f57']")
# documents.click()
item = driver.find_element(By.CSS_SELECTOR, "div[data-list-index='0']")
item.click()

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
