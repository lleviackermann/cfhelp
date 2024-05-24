from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from helpers import codeforces_login
from driver_setup import get_headless_driver, get_head_driver
from selenium.webdriver.chrome.webdriver import WebDriver
from print_texts import display_error_message, display_information, display_success_message, display_processing_message, display_negative_information
from add_problem import is_problemId_correct, get_contestId_problemNumber
from get_compiler_details import is_cval_correct
import time
import os
from dotenv import load_dotenv


MAX_TIME_TO_WAIT = 20
load_dotenv()
CDIR = os.getcwd()
DEFAULT_COMPILER_VALUE = os.getenv("DEFAULT_COMPILER_VALUE")
PROBLEMS_URL = "https://codeforces.com/problemset/problem/"

def handle_problem_submit_arguments(args: list):
    if len(args) < 3:
        display_information("For submitting a problem: ", "cfhelp submit <file> [--pId=<problemId>] [--cVal=<compiler>]")
        return
    
    solution_file_name = args[2]
    solution_file_path = os.path.join(CDIR, solution_file_name)
    if not os.path.exists(solution_file_path):
        display_error_message(f"{solution_file_path} not found! Please enter correct file name!")
        return
    
    problem_id = ""
    compiler_value = DEFAULT_COMPILER_VALUE
    
    # Parse optional arguments
    for arg in args[3:]:
        if arg.startswith("--pId="):
            problem_id = arg.split("=", 1)[1]
        elif arg.startswith("--cVal="):
            try:
                compiler_value = int(arg.split("=", 1)[1])
                if not is_cval_correct(compiler_value):
                    display_error_message(f"{compiler_value} is not correct!")
                    display_information("To see all the valid compiler values run the command: " , "cfhelp get compiler-details")
                    return
            except ValueError:
                display_error_message("Error: Compiler value must be an integer.")
                return
        else:
            display_error_message(f"Invalid argument: {arg}")
            display_information("For submitting a problem: ", "cfhelp submit <file> [--pId=<problemId>] [--cVal=<compiler_value>]")
            return
    
    if problem_id == "":
        if '.' in solution_file_name:
            problem_id = solution_file_name.split(".", 1)[0]
        else:
            display_error_message(f"Invalid solution_file name '{solution_file_name}'. The file name must contain a dot (.) to derive the problem ID.")
            return
        
    contest_id, problem_number = get_contestId_problemNumber(problem_id)
    
    if not is_problemId_correct(contest_id, problem_number):
        display_error_message(f"{solution_file_name} is not in proper format!")
        return 
    else:
        display_success_message(f"ProblemId is correct\n")
    submit_problem(solution_file_path, problem_id, compiler_value, contest_id, problem_number)
    

def submit_problem(solution_file_path, problemId, compiler_value, contest_id, problem_number):
    current_problem_url = PROBLEMS_URL + contest_id + "/" + problem_number
    driver = get_headless_driver()
    display_processing_message(f"\n..........Submitting solution..........")
    driver = codeforces_login(driver)
    if driver == None:
        return
    driver.get(current_problem_url)
    try:
        WebDriverWait(driver, MAX_TIME_TO_WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='sourceFile']")))
        WebDriverWait(driver, MAX_TIME_TO_WAIT).until(EC.presence_of_element_located((By.NAME, "programTypeId")))
        WebDriverWait(driver, MAX_TIME_TO_WAIT).until(EC.presence_of_element_located((By.ID, "sidebarSubmitButton")))
    except TimeoutException as e:
        display_error_message(f"Something went wrong! Please ensure you have proper internet connection and try again!")
        return
    file_select_btn = driver.find_element(By.CSS_SELECTOR, "input[name='sourceFile']")
    file_select_btn.send_keys(solution_file_path)
    compiler_options_menu = driver.find_element(By.NAME, "programTypeId")
    compiler_options_menu = Select(compiler_options_menu)
    compiler_options_menu.select_by_value(str(compiler_value))
    submit_btn = driver.find_element(By.ID, "sidebarSubmitButton")
    submit_btn.click()
    try:
        WebDriverWait(driver, MAX_TIME_TO_WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "td[waiting='true']")))
        display_success_message(f"Solution submitted!\n")
        display_processing_message(f"Waiting for solution verdict!")
        WebDriverWait(driver, 120).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "td[waiting='true']")))
    except Exception as e:
        display_error_message("It is taking too long for verdict! Please check codforces site for your solution verdict or you may have submitted the code without changing it!")
        driver.quit()
        return 
    verdict_element = driver.find_element(By.CSS_SELECTOR, "td[waiting='false']")
    verdict = verdict_element.text
    if verdict == "Accepted":
        display_information("Solution Verdict: ", f"{verdict}")
    else:
        display_negative_information('Solution Verdict: ', f'{verdict}')
    driver.quit()
    