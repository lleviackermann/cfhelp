import time
from helpers import codeforces_login
from driver_setup import get_headless_driver, get_head_driver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import re
PROBLEM_SUBMIT_URL = "https://codeforces.com/problemset/submit"
MAX_TIME_TO_WAIT = 20
CURRENT_FILE_PATH = os.path.realpath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE_PATH)
COMPILER_FILE_DETAILS_PATH = os.path.join(CURRENT_DIR, "compiler_details.txt")

def update_compilers_values():
    driver = get_headless_driver()
    driver = codeforces_login(driver)
    if driver == None:
        return
    driver.get(PROBLEM_SUBMIT_URL)
    WebDriverWait(driver, MAX_TIME_TO_WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='programTypeId']")))
    select_menu = driver.find_element(By.CSS_SELECTOR, "select[name='programTypeId']")
    compilers_options = select_menu.find_elements(By.CSS_SELECTOR, "option")
    compiler_details = ""
    for option in compilers_options:
        compiler_details += option.text + " = " + option.get_attribute('value') + "\n"
    with open(COMPILER_FILE_DETAILS_PATH, 'w') as compiler_file:
        compiler_file.write(compiler_details)
    driver.quit()
    
def is_cval_correct(cval : int):
    numbers = []
    with open(COMPILER_FILE_DETAILS_PATH, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Split the line by '=' and strip any extra whitespace
            parts = line.split('=')
            if len(parts) == 2:
                try:
                    # Extract the number after '='
                    number = int(parts[1].strip())
                    numbers.append(number)
                except ValueError:
                    # If conversion to integer fails, skip this line
                    continue
    if cval in numbers:
        return True
    return False

def get_compiler_details():
    compiler_details = ""
    with open(COMPILER_FILE_DETAILS_PATH, 'r') as file:
        compiler_details = file.read()
    
    print(compiler_details)
    