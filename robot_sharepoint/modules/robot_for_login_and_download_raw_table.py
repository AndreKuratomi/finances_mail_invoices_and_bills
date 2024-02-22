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

from robot_sharepoint.modules.download_directories_management import empty_download_directories, moving_files_from_virtual_dir

from tqdm import tqdm

import ipdb


def robot_for_raw_table(username: str, password: str, site_url: str, 
                        download_dir: str, progress_bar: bool = True) -> None:
    
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

    # time.sleep(10)
    # Hovering an element:
    item = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-selection-index='1']")))
    pbar.update(1)
    item.click()
    pbar.update(1)

    item2 = item.find_element(By.CSS_SELECTOR, "button[data-automationid='FieldRender-DotDotDot']")
    item2.click()
    download = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-automationid='downloadCommand']")))
    pbar.update(1)
    download.click()

    # ipdb.set_trace()

    # Linux:
    # # Create an instance of ActionChains and perform the hover action
    # actions = ActionChains(driver)
    # actions.move_to_element(item).perform()
    # pbar2.update(1)
    # download = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-automationid='downloadCommand']")))
    # download.click()

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

    moving_files_from_virtual_dir(download_dir, default_download_dir)

    # driver.close()
    # display.stop()
