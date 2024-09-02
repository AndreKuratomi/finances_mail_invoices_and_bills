import os
import time

# from datetime import datetime

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.edge.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm

import ipdb

# from robot_sharepoint.modules.robot_utils import unzip_files
from robot_sharepoint.modules.robot_utils.download_directories_management import empty_download_directories, moving_files_from_virtual_dir


def download_attachments_from_sharepoint(user_email: str, password: str, site_url: str, 
                        download_dir: str, cnpj: str, nfe: str, refs: str, progress_bar: bool = True) -> None:
    """Selenium as RPA function that looks for specific files on sharepoint that may serve as email attachments and if found downloads them."""

    default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

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

    # TIME LOGIC:
    year = refs[3:]

    month_from_table = refs[0:2]
    months_list = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
    month_number = int(month_from_table) - 1
    month_name = months_list[month_number]
    month_sharepoint = month_from_table + ' - ' + month_name

    files_list = list()
    
    year = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"button[title='ANO {year}']"))) # lógica para obter ano do calendário
    pbar.update(1)
    year.click()
    pbar.update(1)

    month = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"button[title='{month_sharepoint}']"))) # lógica para obter mês do calendário - 1
    pbar.update(1)
    month.click()
    pbar.update(1)

    # LOOKING FOR CLIENT BY CNPJ:
    client_folder = None
    time.sleep(1)

    try:
        time.sleep(1)

        # Scroll down entire page:
        wait = WebDriverWait(driver, 30)
        scrollable_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-is-scrollable='true']")))

        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

        while True:
            # Scroll down the scrollable element
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
            
            # Wait for new content to load
            time.sleep(1)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
            if new_height == last_height:
                break
            last_height = new_height

        print(cnpj)
        client_folder = driver.find_element(By.XPATH, f"//*[starts-with(@title, '{cnpj}')]")
        print("client_folder:", client_folder)
        if client_folder:
            driver.execute_script("arguments[0].scrollIntoView(true);", client_folder)
            time.sleep(1)

            try:
                # Click using JavaScript
                driver.execute_script("arguments[0].click();", client_folder)
            except ElementClickInterceptedException:
                # If another element is intercepting, find and hide it
                overlaying_element = driver.find_element(By.CSS_SELECTOR, "overlay-element-css-selector")
                driver.execute_script("arguments[0].style.display = 'none';", overlaying_element)
                driver.execute_script("arguments[0].click();", client_folder)
                client_folder.click()
                pbar.update(1)

                time.sleep(1)

            # LOOKING FOR FOLDER BY NFE:
            nfe_folder = None
            try:
                time.sleep(1)
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
                        files_list.append(selectable_icon.accessible_name)

                        time.sleep(1)
                    
                    print(files_list)

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

                    moving_files_from_virtual_dir(default_download_dir, download_dir, files_list)

                else:
                    print("No nfe found for {}!".format(nfe))

            except Exception as e:
                print(f"Error while robot in nef folder: {e}")

        else:     
            raise ModuleNotFoundError("No client found for {}!".format(cnpj))

    except Exception as e:
        print("No client found for {}!".format(cnpj))
        print(f"Error while robot in CNPJ folder: {cnpj}")
