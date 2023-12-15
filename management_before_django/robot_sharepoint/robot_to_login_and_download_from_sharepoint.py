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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm

import ipdb

def robot_for_sharepoint(username: str, password: str, user_id: str, pass_id: str,
                        #   hover_selec: str, download_selec: str, 
                          share_url: str, download_dir: str, progress_bar: bool = True):
    
    # CHECK IF VIRTUAL DOWNLOAD DIR HAS CONTENT AND IF SO EMPTY IT:
    # Tqdm1-3 (Check whether directories are empty):
    if progress_bar:
        pbar1 = tqdm(desc="Check whether directories are empty", total=9)
        pbar1.update(1)

    default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    pbar1.update(1)

    dir_to_origin_path = Path(default_download_dir)
    pbar1.update(1)

    origin_dir_content = list(dir_to_origin_path.iterdir())
    pbar1.update(1)


    if len(origin_dir_content) > 0:
        pbar1.update(1)
        os.remove(default_download_dir)
        pbar1.update(1)

        # shutil.rmtree(default_download_dir) # very agressive...
        # os.mkdir(default_download_dir)


    # CHECK IF DESTINATION DOWNLOAD DIR HAS CONTENT AND IF SO EMPTY IT:
    dir_to_destiny_path = Path(download_dir)
    pbar1.update(1)

    destiny_dir_content = list(dir_to_destiny_path.iterdir())
    pbar1.update(1)

    if len(destiny_dir_content) > 0:
        pbar1.update(1)

        # ipdb.set_trace()
        # os.remove(download_dir)
        shutil.rmtree(download_dir) # very agressive...
        os.mkdir(dir_to_destiny_path)

    pbar1.close()

    # CONNECT TO BROWSER:
    # Tqdm2-3 (Connect to browser and download the file):
    if progress_bar:
        pbar2 = tqdm(desc="Connecting to browser and taking table", total=13)
        pbar2.update(1)

    # Driver instance:
    options = webdriver.EdgeOptions()
    pbar2.update(1)

    # options.add_argument('headless')
    driver = webdriver.Edge(options=options)
    pbar2.update(1)

    # VIRTUAL ATTEMPT TO HIDE ROBOT PAGE:
    # display = Display(visible=0, size=(800, 600))
    # display.start()

    # # ALTERNATIVE WITH MSEDGE.SELENIUM TOOLS, BUT NEED TO DOWNLOAD EDGE AND CONFIGURE IT TO PATH:
    # options = EdgeOptions()
    # options.use_chromium = True
    # options.add_argument(f"--user-data-dir={download_dir}")

    # driver = Edge(options=options)

    # Navigate to Sharepoint login page and maximize its window:
    # driver.get(sharepoint_url)
    driver.get(share_url)
    pbar2.update(1)
    # options.add_argument("--disable-infobars")
    driver.maximize_window()
    pbar2.update(1)

    # LOGIN:
    # Find username input field by its ID and enter email address:
    # username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, username_input_id)))
    username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, user_id)))
    pbar2.update(1)
    # Enter username and submit the form:
    username_input.send_keys(username)
    pbar2.update(1)
    username_input.send_keys(Keys.RETURN)
    pbar2.update(1)

    # Wait for the password input to be visible:
    # password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, password_input_id)))
    password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, pass_id)))
    pbar2.update(1)
    # Enter password and submit the form:
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    pbar2.update(1)
    # Hovering an element:
    item = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-selection-index='1']")))
    # driver.execute_script("arguments[0].hover();", item)
    # item = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, hover_selector)))
    # item = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, hover_selec)))
    item.click()
    pbar2.update(1)
    # Create an instance of ActionChains and perform the hover action
    actions = ActionChains(driver)
    actions.move_to_element(item).perform()
    pbar2.update(1)

    download = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-automationid='downloadCommand']")))
    # driver.execute_script("arguments[0].click();", download)
    # download = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, download_selector)))
    # download = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, download_selec)))
    download.click()
    pbar2.update(1)

    time.sleep(5)

    # CHECKING IF FILE WAS CORRECTLY DOWNLOADED:
    default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    # print(default_download_dir)
    dir_to_path = Path(default_download_dir)
    dir_content = list(dir_to_path.iterdir())
    
    while len(list(Path(default_download_dir).iterdir())) == 0:
        time.sleep(1)
        if progress_bar:
            pbar2.update(1)
    pbar2.close()
    
    # Tqdm3-3 (Move downloaded file):
    if progress_bar:
        # print()
        pbar3 = tqdm(desc="Moving downloaded files", total=9)
        pbar3.update(1)
    for file in dir_content:
        pbar3.update(1)
        if file.is_file():
            pbar3.update(1)
            path_to_table = str(file)
            pbar3.update(1)

            specific_char = "/"
            pbar3.update(1)
            index = path_to_table.rfind(specific_char)
            pbar3.update(1)
            path_content = path_to_table[index+1:]
            pbar3.update(1)
            # print(path_content)
            shutil.move(path_to_table, download_dir)
            pbar3.update(1)
            if progress_bar:
                pbar3.update(1)

        else:
            raise Exception("Something went wrong... check the file itself")
        

    if progress_bar:
        pbar3.close()

    driver.close()
    # display.stop()
