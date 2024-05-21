from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from print_texts import display_error_message, display_success_message
from dotenv import load_dotenv
import os
import time
load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
LOGIN_URL = "https://codeforces.com/enter"
MAX_TIME_TO_WAIT = 20

def check_is_digit(char):
    if ord('0') <= ord(char) <= ord('9'):
        return True
    return False

def check_is_uppercase_alphabet(char):
    if 'A' <= char <= 'Z':
        return True
    return False

def codeforces_login(driver : WebDriver):
    if USERNAME and PASSWORD and USERNAME.strip() != "" and PASSWORD.strip() != "":
        display_error_message("Please make sure you have included username and password into .env sample. Please see the .sample.env file.")
        return None
    try:
        driver.get(LOGIN_URL)
    except Exception as e:
        display_error_message("Failed to load login page.")
        return None

    try:
        WebDriverWait(driver, MAX_TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, "handleOrEmail"))
        )
        WebDriverWait(driver, MAX_TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        WebDriverWait(driver, MAX_TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, "remember"))
        )
    except TimeoutException as e:
        display_error_message("Something went wrong. Please check your internet connection!")
        return None

    try:
        username_input = driver.find_element(By.ID, "handleOrEmail")
        password_input = driver.find_element(By.ID, "password")
        remember_me_checkbox = driver.find_element(By.ID, "remember")
        login_button = driver.find_element(By.CSS_SELECTOR, "input[value='Login']")
    except NoSuchElementException as e:
        display_error_message("Something went wrong. Please check your internet connection!.")
        return None

    try:
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        remember_me_checkbox.click()
        login_button.click()
    except Exception as e:
        display_error_message("An error occurred while trying to fill in the login form and submit it. Please check your username and password in the .env file.")
        return None

    try:
        WebDriverWait(driver, MAX_TIME_TO_WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jGrowl-notification .message")))
    except TimeoutException as e:
        display_error_message("Login failed or took too long. Please check your username and password!")
        return None

    return driver