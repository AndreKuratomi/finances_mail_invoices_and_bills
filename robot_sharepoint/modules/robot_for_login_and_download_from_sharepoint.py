import os

import requests
import shutil
import time

from pathlib import Path

from pyvirtualdisplay import Display
# from msedge.selenium_tools import Edge, EdgeOptions

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.edge.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm

import ipdb

from robot_sharepoint.modules import unzip_files
from robot_sharepoint.modules.download_directories_management import empty_download_directories, moving_files_from_virtual_dir


def robot_for_sharepoint(username: str, password: str, user_id: str, pass_id: str,
                          site_url: str, download_dir: str, cnpj: str, nfe: str, progress_bar: bool = True):
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
    # options = webdriver.EdgeOptions()
    # options.use_chromium = True
    # options.add_argument('--headless=new')
    # options.add_argument('--no-sandbox')

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
    username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, user_id)))
    pbar.update(1)

    username_input.send_keys(username)
    pbar.update(1)
    username_input.send_keys(Keys.RETURN)
    pbar.update(1)


    password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, pass_id)))
    pbar.update(1)

    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    pbar.update(1)

    # CLICKING FOLDERS:
    root_folder = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='01 - MEDIÇÕES']")))
    pbar.update(1)
    root_folder.click()
    pbar.update(1)

    year = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='ANO 2024']")))
    pbar.update(1)
    year.click()
    pbar.update(1)

    month = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='01 - JANEIRO']")))
    pbar.update(1)
    month.click()
    pbar.update(1)

    # Looking for client by CNPJ:
    client_folder = None
    time.sleep(1)

    try:
        client_folder = driver.find_element(By.XPATH, f"//*[starts-with(@title, '{cnpj}')]")
        # print(client_folder)

    except:
        print("No client found for {}!".format(cnpj))

    if client_folder:
        client_folder.click()
        pbar.update(1)

        time.sleep(1)

        # Looking for folder by NFE:
        nfe_folder = None
        try:
            nfe_folder = driver.find_element(By.XPATH, f"//*[starts-with(@title, '{nfe}')]")
        except:
            print("No nfe found for {}!".format(nfe))
        
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
                # time.sleep(1)
                download_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-automationid='downloadCommand']")))
                download_button.click()

                # Unclick the element!
                selectable_icon.click()
                # ipdb.set_trace()

                time.sleep(1)
            
            # download_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-automationid='downloadCommand']")))
            # download_button.click()
            # pbar.update(1)

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

            # for file in tqdm(default_download_dir_list, "Checking if the download is really complete..."):
            #     print(file)
            #     while any(file.suffix == '.crdownload'):
            #         time.sleep(1)

            # while any(file.suffix == '.crdownload' for file in Path(default_download_dir).iterdir()):
            #     time.sleep(1)
                # if file.suffix == '.crdownload':
# while any(file.suffix == '.crdownload' for file in Path(download_dir).iterdir()):
#         time.sleep(1)
#         if progress_bar:
#             pbar.update(1

            driver.quit()

            moving_files_from_virtual_dir(download_dir, default_download_dir)

            # # Unzip files:
            # unzip_files.unzipfile(download_dir)

        else:
            print("No nfe found for {nfe}!")

    else:
        print("No client found for {cnpj}!")
