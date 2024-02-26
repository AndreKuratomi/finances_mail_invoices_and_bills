import time

from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm

import ipdb


def upload_files_to_sharepoint(username: str, password: str, reports_path: Path, site_url: str, progress_bar: bool = True) -> None:
    # CONNECT TO BROWSER:
    if progress_bar:
        pbar = tqdm(desc="Connecting to browser and uploading file", total=0)

    # Driver instance:
    options = Options()
    # options.add_argument('--headless=new')
    options.add_argument('-inprivate')

    driver = webdriver.Edge(options=options)
    driver.get(site_url)
    driver.maximize_window()

    # LOGIN:
    username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "input")))
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)

    password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    # UPLOADING FILE:
    item = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "i[data-icon-name='More']")))
    time.sleep(1)
    item.click()

    upload = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[title='Carregar arquivos do seu computador para este local']")))

    # Create an instance of ActionChains and perform the hover action
    actions = ActionChains(driver)
    actions.move_to_element(upload).perform()
    item2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='Arquivos']")))
    item2.click()
    time.sleep(2)

    # Dialog page!:
    file_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='file']")))
    # driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    
    # Extract info from attachments:
    tables_path_content = list(Path(reports_path).iterdir())    
    # Attach files to email:
    for file in tables_path_content:
        print(file)
        stringfy = str(file.resolve())
        print(stringfy)
        if stringfy.endswith(".txt"):
            try:
                time.sleep(1)
                file_input.send_keys(stringfy)
                print("OK!")
                ipdb.set_trace()
                time.sleep(3)
                
            except StaleElementReferenceException:
                ipdb.set_trace()
                file_input.send_keys(Keys.ESCAPE)
                print("IRK!")
                item = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "i[data-icon-name='More']")))
                time.sleep(1)
                item.click()

                upload = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[title='Carregar arquivos do seu computador para este local']")))

                # Create an instance of ActionChains and perform the hover action
                actions = ActionChains(driver)
                actions.move_to_element(upload).perform()
                item2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='Arquivos']")))
                item2.click()
                time.sleep(2)

                # Dialog page!:
                file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                # file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                file_input.send_keys(stringfy)
                print("OK!2")
                file_input.send_keys(Keys.ESCAPE)
    # ipdb.set_trace()

    driver.quit()
