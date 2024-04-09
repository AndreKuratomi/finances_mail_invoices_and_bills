import time

from datetime import datetime
from pathlib import Path

from selenium import webdriver
# from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm

import ipdb


def upload_files_to_sharepoint(user_email: str, password: str, reports_path: Path, site_url: str, progress_bar: bool = True) -> None:

    
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
    user_email_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "input")))
    user_email_input.send_keys(user_email)
    user_email_input.send_keys(Keys.RETURN)

    password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    # CLICKING FOLDERS:
    reports = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='15 - RELATÓRIOS DE ENVIO']")))
    pbar.update(1)
    reports.click()
    pbar.update(1)

    # TIME LOGIC:
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")

    months_list = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']
    month_number = int(month) - 1
    month_name = months_list[month_number]

    mes_sharepoint = month + ' ' + month_name

    year = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"button[title='ANO {year}']")))
    # year = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='ANO 2024']")))
    pbar.update(1)
    year.click()
    pbar.update(1)


    month = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='JANEIRO']")))
    # month = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"button[title='{mes_sharepoint}']")))
    pbar.update(1)
    month.click()
    pbar.update(1)

    time.sleep(1)

    # UPLOADING FILE:
    upload = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='Carregar arquivos do seu computador para este local']")))
    upload.click()
 
    time.sleep(1)

    # ipdb.set_trace()
    # upload_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automationid='uploadFileCommand']")))
    # upload_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='Arquivos']")))
    upload_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Arquivos']")))
    upload_button.click()
    time.sleep(2)

    # Dialog page!:
    file_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='file']")))
    
    # Extract final report from reports and upload it:
    tables_path_content = list(Path(reports_path).iterdir())

    for file in tables_path_content:
        stringfy = str(file.resolve())
        print('file:', file)
        print('stringfy:', stringfy)
        if stringfy.endswith("relatorio_diario.txt"):
            try:
                time.sleep(1)
                file_input.send_keys(stringfy)
                time.sleep(3)
                
            except Exception as e:
                print(e) 

    driver.quit()
