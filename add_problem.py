from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from helpers import check_is_digit, check_is_uppercase_alphabet
from print_texts import display_error_message, display_processing_message, display_success_message, display_information
import re
import requests
import os
import json

options = webdriver.ChromeOptions()
options.add_argument("--headless") 
    
PROBLEMS_URL = "https://codeforces.com/problemset/problem/"
CONTESTS_URL =   "https://codeforces.com/contest/"
CONTEST_API = "https://codeforces.com/api/contest.standings?count=1&contestId="
SUPPORTED_PROGRAMMING_LANGUAGE = ["c", "cpp"]
MAX_TIME_TO_WAIT = 15
CURRENT_FILE_PATH = os.path.realpath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE_PATH)

def get_contestId_problemNumber(problem_id):
    contest_id = ""
    problem_number = ""
    flag = 0
    for letter in problem_id:
        if check_is_digit(letter) and flag == 0:
            contest_id += letter
        elif check_is_uppercase_alphabet(letter) or flag == 1:
            flag = 1
            problem_number += letter
    return contest_id, problem_number

def formatted_problem_title(problem_title):
    cleaned_title = re.sub(r'[^\w\s.]', '', problem_title)
    formatted_title = cleaned_title.replace(' ', '_')
    return formatted_title

def is_problemId_correct(contest_id, problem_number):
    display_processing_message(f"Checking if the provided problem id is correct or not..........")
    contest_link = CONTEST_API + contest_id
    response = requests.get(contest_link)
    data = response.json()
    if response.status_code == 200:
        try:
            assert data['status'] == "OK"
            problems = data['result']['problems']
            for problem in problems:
                if problem['index'] == problem_number:
                    return True
        except AssertionError: 
            return False
    return False

def check_for_programming_lang(programming_language):
    if programming_language not in SUPPORTED_PROGRAMMING_LANGUAGE:
        return False
    return True

def get_sample_tests(new_problem_url):
    problem_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    display_processing_message("Downloading sample test cases for the given problem Id...........")
    try:
        problem_driver.get(new_problem_url)
        WebDriverWait(problem_driver, MAX_TIME_TO_WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".problem-statement .header > .title")))
        WebDriverWait(problem_driver, MAX_TIME_TO_WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sample-tests")))
        problem_title = problem_driver.find_element(By.CSS_SELECTOR, ".problem-statement .header > .title").text
    except TimeoutException:
        display_error_message("Page took too long to load! Please check your network connection")
        problem_driver.quit()
        return None
    except NoSuchElementException:
        display_error_message("Problem elements not found on the page!")
        problem_driver.quit()
        return None
    except Exception as e:
        display_error_message(f"An error occurred: {e}! Please try again!")
        problem_driver.quit()
        return None
    sample_tests = problem_driver.find_element(By.CSS_SELECTOR, ".sample-tests")
    return sample_tests, problem_title

def make_sample_tests(sample_tests, problem_id):
    try:
        inputs = sample_tests.find_elements(By.CSS_SELECTOR, ".input")
        outputs = sample_tests.find_elements(By.CSS_SELECTOR, ".output")
        
        if not inputs or not outputs:
            raise ValueError("No input or output elements found in the sample tests.")
        
        if len(inputs) != len(outputs):
            raise ValueError("Something went wrong while copying the sample tests! Please try again!")
        
        directory_path = os.path.join(CURRENT_DIR, "sample_tests")
        try:
            os.makedirs(directory_path, exist_ok=True)
            problem_sample_file_name = problem_id + ".json"
            problem_sample_file_path = os.path.join(directory_path, problem_sample_file_name)
            
            sample_tests_data = []
            
            for i, (input_element, output_element) in enumerate(zip(inputs, outputs)):
                input_text = input_element.find_element(By.CSS_SELECTOR, "pre").text
                output_text = output_element.find_element(By.CSS_SELECTOR, "pre").text
                sample_tests_data.append({
                    "test_number": i + 1,
                    "input": input_text,
                    "output": output_text
                })
                
            with open(problem_sample_file_path, 'w') as json_file:
                json.dump(sample_tests_data, json_file, indent=4)

            return 1
        except Exception as e:
            display_error_message(f"An error occurred while creating the directory / file. Please try again!")
            return 0
    
    except NoSuchElementException as e:
        display_error_message(f"An error occurred while locating elements. Please try again! {e}")
        return 0
    except ValueError as e:
        display_error_message(f"{e}")
        return 0
    except Exception as e:
        display_error_message(f"An unexpected error occurred: {e}")
        return 0
    return 1

def add_problem(problem_id, programming_language="cpp"):
    contest_id, problem_number = get_contestId_problemNumber(problem_id)
    if not check_for_programming_lang(programming_language):
        display_error_message(f"{programming_language} is not supported! Only C and CPP are language are supported!")
        return 
    if not is_problemId_correct(contest_id, problem_number):
        display_error_message(f"{problem_id} is incorrect! Please provide correct problem id!")
        return 
    else:
        display_success_message(f"{problem_id} is correct!")
        
    new_problem_url = PROBLEMS_URL + contest_id + "/" + problem_number
    result = get_sample_tests(new_problem_url)
    if result is None:
        return
    sample_tests, problem_title = result
    solution_file_name = contest_id + problem_title + "." + programming_language
    solution_file_name = formatted_problem_title(solution_file_name)
    with open(solution_file_name, 'w') as file:
        pass
    if make_sample_tests(sample_tests, problem_id) == 0:
        return
    else:
        display_success_message(f"Testcases downloaded successfully.")
        display_information("Run", f"cfhelp test {solution_file_name}", "to test the solution against the sample tests!", bold=True, italic=True)
    