import os
import time

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.edge.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from robot_sharepoint.modules.robot_utils.download_directories_management import empty_download_directories, moving_files_from_virtual_dir

from tqdm import tqdm

import ipdb


def robot_for_raw_table(username: str, password: str, site_url: str, 
                        download_dir: str, progress_bar: bool = True) -> None:
    
    # print("CNPJ:", cnpj)
    print("sharepoint_robot:", __name__)

    default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    empty_download_directories(download_dir, default_download_dir)
    # ipdb.set_trace()

    # CONNECT TO BROWSER:
    if progress_bar:
        pbar = tqdm(desc="Connecting to browser and taking content", total=15)
        pbar.update(1)

    # Driver instance:
    options = Options()
    options.add_argument('--headless=new')

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
    username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "input")))
    pbar.update(1)

    username_input.send_keys(username)
    pbar.update(1)
    username_input.send_keys(Keys.RETURN)
    pbar.update(1)


    password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    pbar.update(1)

    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    pbar.update(1)

    # CLICKING FOLDERS:
    reports = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='14 - BASE DE DADOS']")))
    pbar.update(1)
    reports.click()
    pbar.update(1)

    year = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='ANO 2024']")))
    pbar.update(1)
    year.click()
    pbar.update(1)

    month = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='JANEIRO']"))) # criar lógica para obter mês do calendário - 1
    pbar.update(1)
    month.click()
    pbar.update(1)


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
        # ipdb.set_trace()

        # Unclick the element!
        selectable_icon.click()

        time.sleep(1)

    pbar.update(1)
    time.sleep(1)
    pbar.update(1)
    time.sleep(1)
    
    while len(list(Path(default_download_dir).iterdir())) == 0:
        time.sleep(1)
        if progress_bar:
            pbar.update(1)
    pbar.close()
    driver.quit()
    # ipdb.set_trace()
    print("download_dir:", download_dir)
    moving_files_from_virtual_dir(download_dir, default_download_dir)

    # driver.close()
    # display.stop()
