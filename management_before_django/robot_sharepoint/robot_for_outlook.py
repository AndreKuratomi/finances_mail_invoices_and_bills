import os

import requests
import shutil
import stat
import time

from dotenv import load_dotenv

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.edge.options import Options

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm

import ipdb

load_dotenv()

# .envs:
outlook_url = os.getenv("OUTLOOK_URL")
user_outlook = os.getenv("USER_OUTLOOK")
user_outlook_password = os.getenv("USER_OUTLOOK_PASSWORD")

def robot_for_outlook(username: str, password: str, user_id: str, pass_id: str,
                        hover_selec: str, download_selec: str, 
                        outlook_url: str, download_dir: str, progress_bar: bool = True):
    
    # CONNECT TO BROWSER:
    # Tqdm2-3 (Connect to browser and download the file):
    if progress_bar:
        pbar2 = tqdm(desc="Connecting to browser and taking table", total=15)
        pbar2.update(1)

    # Driver instance:
    options = Options()
    # options.add_argument('--headless=new')

    # For Windows OS:
    options.add_argument('-inprivate')
    pbar2.update(1)

    driver = webdriver.Edge(options=options)
    pbar2.update(1)

    # Navigate to Sharepoint login page and maximize its window:
    driver.get(outlook_url)
    pbar2.update(1)
    # options.add_argument("--disable-infobars")
    driver.maximize_window()
    pbar2.update(1)


    # LOGIN:
    # Find username input field by its ID and enter email address:
    # username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, username_input_id)))
    username_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, user_id)))
    pbar2.update(1)

    # Enter username and submit the form:
    username_input.send_keys(username)
    pbar2.update(1)
    username_input.send_keys(Keys.RETURN)
    pbar2.update(1)

    # Wait for the password input to be visible and then enter password and submit the form:
    # password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, password_input_id)))
    password_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, pass_id)))
    pbar2.update(1)

    # Enter password and submit the form:
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    pbar2.update(1)

    # INSIDE OUTLOOK:

    # Pesquisar input:
    input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Pesquisar']")))
    pbar2.update(1)

    time.sleep(3)

    input.send_keys("017919")
    pbar2.update(1)
    input.send_keys(Keys.RETURN)
    pbar2.update(1)

    time.sleep(1)

    # Email found click:
    email = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label*='nfe.noreply@barueri.sp.gov.br']")))

    #     # Wait for the element to become stale:
    # WebDriverWait(driver, 30).until(EC.staleness_of(email))

    #     # Wait for the element to re-appear:
    # email = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label*='nfe.noreply@barueri.sp.gov.br']")))
    email.click()

    time.sleep(1)

    answer_all_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Responder a todos']")))
    answer_all_button.click()

    # attach_button = WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='Anexar arquivo']")))
    attach_button = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='Anexar arquivo']")))
    time.sleep(2)
    attach_button.click()

    
    # Wait for the element to become stale:
    # WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='Anexar arquivo']")))
    # WebDriverWait(driver, 30).until(EC.staleness_of(attach_button))
    # attach_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Anexar arquivo']")))
    time.sleep(2)
    what_to_attach_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='Carregar e compartilhar']")))
    print(what_to_attach_button)
    if StaleElementReferenceException:
        print("NOT HERE")
        WebDriverWait(driver, 50).until(EC.staleness_of(attach_button))
        what_to_attach_button.click()
    else: 
        what_to_attach_button.click()

    time.sleep(2)
    dialog_box = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "dialog[role='dialog']")))
    driver.switch_to.default_content()
    driver.switch_to.frame(dialog_box.find_element(By.CSS_SELECTOR, "iframe[title='OneDrive']"))
    ipdb.set_trace()
    
    print(len(driver.window_handles))
    driver.switch_to.window(driver.window_handles[1])
    # driver.switch_to.window('Abrir')

    # Create an instance of ActionChains and perform the hover action
    # actions = ActionChains(driver)
    # actions.move_to_element(attach_button).perform()
    # pbar2.update(1)

    # what_to_attach_button = WebDriverWait(driver, 10).until(By.CSS_SELECTOR, "button[name='Carregar e compartilhar']")

    # # Wait for another element to become stale:
    # WebDriverWait(driver, 10).until(EC.staleness_of(what_to_attach_button))

    # Wait for another element to re-appear:

    

    # download = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-automationid='downloadCommand']")))
    # pbar2.update(1)
    # download.click()

    # # CHECK IF VIRTUAL DOWNLOAD DIR HAS CONTENT AND IF SO EMPTY IT:
    # # Tqdm1-3 (Check whether directories are empty):
    # if progress_bar:
    #     pbar1 = tqdm(desc="Check whether directories are empty", total=13)
    #     pbar1.update(1)

    # default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    # pbar1.update(1)

    # dir_to_origin_path = Path(default_download_dir)
    # pbar1.update(1)

    # origin_dir_content = list(dir_to_origin_path.iterdir())
    # pbar1.update(1)

    # print(origin_dir_content)
    # print(default_download_dir)

    # if len(origin_dir_content) > 0:
    #     # ipdb.set_trace()
    #     pbar1.update(1)
    #     # os.remove(default_download_dir)

    #     # Windows:
    #     # Grant default_download_dir read, write and execute permissions:
    #     os.chmod(default_download_dir, stat.S_IRWXU)
    #     pbar1.update(1)

    #     shutil.rmtree(default_download_dir) # very agressive...
    #     pbar1.update(1)

    #     os.mkdir(default_download_dir)
    #     pbar1.update(1)


    # # CHECK IF DESTINATION DOWNLOAD DIR HAS CONTENT AND IF SO EMPTY IT:
    # # ipdb.set_trace()
    # dir_to_destiny_path = Path(download_dir)
    # pbar1.update(1)

    # destiny_dir_content = list(dir_to_destiny_path.iterdir())
    # pbar1.update(1)

    # if len(destiny_dir_content) > 0:
    #     pbar1.update(1)
    #     shutil.rmtree(download_dir) # very agressive...

    #     pbar1.update(1)
    #     os.mkdir(dir_to_destiny_path)
    #     pbar1.update(1)

    # pbar1.close()


    # # time.sleep(10)
    # # Hovering an element:
    # item = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-selection-index='1']")))
    # pbar2.update(1)
    # item.click()
    # pbar2.update(1)

    # item2 = item.find_element(By.CSS_SELECTOR, "button[data-automationid='FieldRender-DotDotDot']")
    # item2.click()
    # download = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-automationid='downloadCommand']")))
    # pbar2.update(1)
    # download.click()

    # # ipdb.set_trace()

    # # Linux:
    # # # Create an instance of ActionChains and perform the hover action
    # # actions = ActionChains(driver)
    # # actions.move_to_element(item).perform()
    # # pbar2.update(1)
    # # download = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-automationid='downloadCommand']")))
    # # download.click()

    # time.sleep(1)
    # pbar2.update(1)
    # time.sleep(1)
    
    # while len(list(Path(default_download_dir).iterdir())) == 0:
    #     time.sleep(1)
    #     if progress_bar:
    #         pbar2.update(1)
    # pbar2.close()
    # driver.quit()
    # # ipdb.set_trace()

    # # CHECKING IF FILE WAS CORRECTLY DOWNLOADED:
    # default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    # print(default_download_dir)
    # dir_to_path = Path(default_download_dir)
    # dir_content = list(dir_to_path.iterdir())
    
    # # Tqdm3-3 (Move downloaded file):
    # if progress_bar:
    #     pbar3 = tqdm(desc="Moving downloaded files", total=9)
    #     pbar3.update(1)

    # for file in dir_content:
    #     pbar3.update(1)
    #     if file.is_file():
    #         pbar3.update(1)
    #         path_to_table = str(file)
    #         pbar3.update(1)

    #         shutil.move(path_to_table, download_dir)
    #         pbar3.update(1)

    #         if progress_bar:
    #             pbar3.update(1)

    #     else:
    #         raise Exception("Something went wrong... check the file itself")
        

    if progress_bar:
        pbar3.close()

    # driver.close()
    # display.stop()
