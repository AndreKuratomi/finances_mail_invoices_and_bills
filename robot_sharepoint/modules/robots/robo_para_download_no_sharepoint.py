import os
import time

from datetime import datetime

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.edge.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm

import ipdb

from robot_sharepoint.modules.robot_utils import unzip_files
from robot_sharepoint.modules.robot_utils.download_directories_management import empty_download_directories, moving_files_from_virtual_dir


def download_anexos_no_sharepoint(user_email: str, password: str, site_url: str, 
                        download_dir: str, cnpj: str, nfe: str, refs: str, progress_bar: bool = True) -> None:
    
    # print("CNPJ:", cnpj)
    print("sharepoint_robot:", __name__)

    default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    empty_download_directories(download_dir, default_download_dir)

    # CONNECT TO BROWSER:
    if progress_bar:
        pbar = tqdm(desc="Connecting to browser and taking content", total=15)
        pbar.update(1)

    # Driver instance:
    options = Options()
    # options.add_argument('--headless=new')

    # For Windows OS:
    options.add_argument('-inprivate')
    pbar.update(1)

    driver = webdriver.Edge(options=options)
    pbar.update(1)

    # Navigate to Sharepoint login page and maximize its window:
    driver.get(site_url)
    pbar.update(1)
    # options.add_argument("--disable-infobars")

    driver.maximize_window()
    pbar.update(1)

    # LOGIN:
    user_email_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "input")))
    pbar.update(1)

    user_email_input.send_keys(user_email)
    pbar.update(1)
    user_email_input.send_keys(Keys.RETURN)
    pbar.update(1)


    password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    pbar.update(1)

    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    pbar.update(1)

    # TIME LOGIC:

    year = refs[3:]

    month = refs[0:2]
    months_list = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']
    month_number = int(month) - 1
    month_name = months_list[month_number]
    mes_sharepoint = month + ' - ' + month_name
    
    # CLICKING FOLDERS:
    # root_folder = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='01 - MEDIÇÕES']")))
    # pbar.update(1)
    # root_folder.click()
    # pbar.update(1)
    
    # year = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title=f'ANO {year}']"))) # lógica para obter ano do calendário
    # pbar.update(1)
    # year.click()
    # pbar.update(1)

    month = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"button[title='{mes_sharepoint}']"))) # lógica para obter mês do calendário - 1
    pbar.update(1)
    month.click()
    pbar.update(1)

    # LOOKING FOR CLIENT BY CNPJ:
    client_folder = None
    time.sleep(1)

    try:
        client_folder = driver.find_element(By.XPATH, f"//*[starts-with(@title, '{cnpj}')]")
        # print(client_folder)

        if client_folder:
            client_folder.click()
            pbar.update(1)

            time.sleep(1)

            # LOOKING FOR FOLDER BY NFE:
            nfe_folder = None
            try:
                nfe_folder = driver.find_element(By.XPATH, f"//*[starts-with(@title, '{nfe}')]")
            
                if nfe_folder:
                    nfe_folder.click()
                    pbar.update(1)

                    time.sleep(1)

                    # Select all items to download:

                    files_to_download_amount = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='ms-List']")))
                    files_to_download_list = files_to_download_amount.find_elements(By.CSS_SELECTOR, "div[class='ms-List-cell']")

                    pbar.update(1)
                    for file in tqdm(files_to_download_list, "Selecting files to download..."):
                        # Create an instance of ActionChains and perform the hover action
                        actions = ActionChains(driver)
                        actions.move_to_element(file).perform()

                        selectable_icon = file.find_element(By.CSS_SELECTOR, "div[role='gridcell']")
                        selectable_icon.click()

                        pre_download_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "i[data-icon-name='More']")))
                        pre_download_button.click()

                        download_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='Baixar']")))
                        download_button.click()

                        # Unclick the element!
                        selectable_icon.click()

                        time.sleep(1)

                    time.sleep(1)
                    pbar.update(1)
                    time.sleep(1)
                    
                    default_download_dir_list = list(Path(default_download_dir).iterdir())

                    while len(default_download_dir_list) == 0:
                        time.sleep(1)
                        if progress_bar:
                            pbar.update(1)
                    pbar.close()
                    
                    time.sleep(1)

                    driver.quit()

                    moving_files_from_virtual_dir(download_dir, default_download_dir)
                
                else:
                    print("No nfe found for {}!".format(nfe))

            except Exception as e:
                print(f"Error while robot in nef folder: {e}")

        else:        
            print("No client found for {}!".format(cnpj))

    except Exception as e:
        print("No client found for {}!".format(cnpj))
        print(f"Error while robot in CNPJ folder: {cnpj}")
