from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm

import ipdb


def recursive_robot(username: str, share_url: str, progress_bar: bool = True):

    # Dictionary to store input ids:
    dict = {"user_input_id": "", "password_input_id": ""}
    
    # CONNECT TO BROWSER:
    # Tqdm (Connect to browser and download the file):
    if progress_bar:
        pbar = tqdm(desc="Connecting to browser and taking ids", total=9)
        pbar.update(1)

    # Driver instance:
    options = webdriver.EdgeOptions()
    options.add_argument('headless')
    # For Windows OS:
    options.add_argument('-inprivate')

    pbar.update(1)

    # options.add_argument('headless')
    driver = webdriver.Edge(options=options)
    pbar.update(1)

    # driver = webdriver.Edge(options=options)

    # Navigate to Sharepoint login page and maximize its window:
    driver.get(share_url)
    driver.maximize_window()
    pbar.update(1)


    # # CHECK IF IT IS LOGGED AND IF SO UNLOGS:
    # if "https://jcgestaoderiscos.sharepoint.com/sites/testes.desenvolvimento/SitePages/Home.aspx" in driver.current_url:
    #     print("oi")

    #     pre_logout_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[id='O365_MainLink_Me']")))
    #     pre_logout_link.click()
    #     pbar.update(1)

    #     logout_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[id='mectrl_body_signOut']")))
    #     logout_link.click()
    #     pbar.update(1)

    #     driver.quit()
    # ipdb.set_trace()


    # # Driver instance:
    # options = webdriver.EdgeOptions()
    # # options.add_argument('headless')
    # pbar.update(1)

    # # options.add_argument('headless')
    driver = webdriver.Edge(options=options)
    # pbar.update(1)

    # # driver = webdriver.Edge(options=options)

    # Navigate to Sharepoint login page and maximize its window:
    driver.get(share_url)
    driver.maximize_window()
    pbar.update(1)

    # LOGIN:
    # Find username input field by its ID and enter email address:
    username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "input")))
    # ipdb.set_trace()
    pbar.update(1)

    # Enter username and submit the form:
    username_input_id = username_input.get_attribute("id")
    dict["user_input_id"] = username_input_id
    pbar.update(1)

    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)
    pbar.update(1)

    # Wait for the password input to be visible:
    password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    # password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, pass_id)))
    pbar.update(1)

    # Enter password and submit the form:
    password_input_id = password_input.get_attribute("id")
    dict["password_input_id"] = password_input_id
    pbar.update(1)
    # driver.close()
    driver.quit()
    # ipdb.set_trace()

    return dict
