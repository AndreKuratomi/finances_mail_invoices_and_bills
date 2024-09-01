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

from tqdm import tqdm

from robot_sharepoint.modules.robot_utils.download_directories_management import empty_download_directories, moving_files_from_virtual_dir

import ipdb


def download_contacts_from_sharepoint(user_email: str, password: str, site_url: str, 
                        download_dir: str, progress_bar: bool = True) -> None:
    """Selenium as RPA function that looks for specific spreadsheet on sharepoint that has clients' contacts (email) info and if found downloads it."""

    print("sharepoint_robot:", __name__)

    default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    # Delete downloaded files in 'raw_table/':
    empty_download_directories(download_dir, default_download_dir)

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

    # CLICKING FOLDERS:
    reports = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='14 - BASE DE DADOS']")))
    pbar.update(1)
    reports.click()
    pbar.update(1)

    time.sleep(1)

    try:
        files_to_download_amount = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='ms-List']")))
        files_to_download_list = files_to_download_amount.find_elements(By.CSS_SELECTOR, "div[class='ms-List-cell']")
        pbar.update(1)

        # Logic for taking off file downloaded from 'default_download' and inserting it in raw_table/:
        files_list = list()

        count = 0

        for file in tqdm(files_to_download_list, "Selecting files to download..."):
            if count == 0:
                count += 1
                continue
            else:
                # Create an instance of ActionChains and perform the hover action
                actions = ActionChains(driver)
                actions.move_to_element(file).perform()

                selectable_icon = file.find_element(By.CSS_SELECTOR, "div[role='gridcell']")
                selectable_icon.click()

                pre_download_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "i[data-icon-name='More']")))
                pre_download_button.click()

                download_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='Baixar']")))
                download_button.click()

                files_list.append(selectable_icon.accessible_name)

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

        print("download_dir:", download_dir)
        moving_files_from_virtual_dir(default_download_dir, download_dir, files_list)

    except:
        print("No contacts table found!")