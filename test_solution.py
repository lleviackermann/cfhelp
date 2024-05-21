import json
import subprocess
import os
from print_texts import display_error_message, display_success_message, display_processing_message, display_information, display_purple_text
from add_problem import get_contestId_problemNumber

CURRENT_FILE_PATH = os.path.realpath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE_PATH)

def compile_c_program(solution_file : str):
    try:
        extension = solution_file.split(".")[-1]
        compiler = "g++"
        if extension == "c":
            compiler = "gcc"
        elif extension != "cpp":
            display_error_message(f"Can't compile .{extension} file. Only supported languages are C and CPP.")
            return False
            
        display_processing_message(f"............Compiling {solution_file}................")
        
        result = subprocess.run([compiler, solution_file, '-o', 'compiled_program', "-DONLINE_JUDGE"], capture_output=True, text=True)
        if result.returncode != 0:
            display_error_message("Compilation failed:")
            display_error_message(result.stderr)
            print()
            return False
        else:
            display_success_message("Compilation successful.\n")
            return True
    except Exception as e:
        display_error_message(f"Error during compilation: {e}\n\n")
        return False

def run_c_program(input_data):
    try:
        result = subprocess.run(['./compiled_program'], input=input_data, text=True, capture_output=True, timeout=10)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Timeout: Program took too long to execute."
    except Exception as e:
        return f"Error: {e}"

def compare_outputs(actual_output, expected_output):
    return actual_output == expected_output

def test_solution_file(solution_file : str):
    problem_id = solution_file.split(".")[0]
    contest_id, problem_number = get_contestId_problemNumber(problem_id)
        
    display_processing_message(f"..........Checking if testcases for {problem_id} are downloaded locally or not.........")
    sample_tests_json_dir_path = os.path.join(CURRENT_DIR, "sample_tests")
    problem_sample_tests_json_file_path = os.path.join(sample_tests_json_dir_path, problem_id + ".json")
    if not os.path.exists(problem_sample_tests_json_file_path):
        display_error_message(f"No sample tests for the given file found!")
        display_information("Please run ", f"cfhelp add-problem {problem_id}", " first to download the testcases locally\n\n", bold=True, italic=True)
        return
    else:
        display_success_message(f"Found the testcases for problem id {problem_id}!\n")

    compiled = compile_c_program(solution_file)
    if not compiled:
        display_error_message("Compilation failed. Exiting.\n")
        return
    
    with open(problem_sample_tests_json_file_path, "r") as file:
        sample_tests_data = json.load(file)
    
    display_purple_text(f"Running the {solution_file} against sample test cases!\n")
    count = 0
    for test_case in sample_tests_data:
        display_information("", f"---------------Sample Test {test_case['test_number']}---------------", bold=True, italic=True)
        test_input = test_case["input"]
        expected_output = test_case["output"]
        
        actual_output = run_c_program(test_input)

        result = compare_outputs(actual_output, expected_output)
        if result:
            display_information(f"Sample Test {test_case['test_number']}: ", "Passed\n", bold=True, italic=True)
            count += 1
        else:
            display_error_message(f"Sample Test {test_case['test_number']}: Failed")
            display_success_message(f"Expected Output: {expected_output}")
            display_error_message(f"Actual Output: {actual_output}")

    os.remove('compiled_program')

    if count == len(sample_tests_data):
        display_information("All Available test cases", "Passed\n", bold=True, italic=True)
        display_information("Run ", f"cfhelp submit {solution_file}", " to submit the solution onto codeforces!", bold=True, italic=True)
    else:
        display_error_message(f"{count} sample test case passed and {len(sample_tests_data) - count} sample test case failed!")
        
