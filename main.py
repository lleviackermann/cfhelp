import sys
from add_problem import add_problem
from print_texts import display_error_message, display_processing_message, display_success_message
from test_solution import test_solution_file
from get_compiler_details import update_compilers_values, get_compiler_details
from submit import handle_problem_submit_arguments

if __name__ == "__main__":
    if len(sys.argv) == 1:
        display_success_message("cfhelp installed successfully")
    elif len(sys.argv) >= 3 and sys.argv[1] == "add-problem":
        if len(sys.argv) == 3:
            add_problem(sys.argv[2])
        elif len(sys.argv) == 4 and sys.argv[3].split('=')[0] == "--ext":
            add_problem(sys.argv[2], sys.argv[3].split('=')[1])
        else:
            display_error_message("Invalid arguments! Please provide proper arguments!")
    elif len(sys.argv) == 3 and sys.argv[1] == "test":
        test_solution_file(sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] == "update-compilers":
        update_compilers_values()
    elif len(sys.argv) == 3 and sys.argv[1] == "get" and sys.argv[2] == "compiler-details":
        get_compiler_details()
    elif len(sys.argv) >= 3 and sys.argv[1] == "submit":
        handle_problem_submit_arguments(sys.argv)
    else:
        display_error_message(f"Please provide proper command line arguments. Check out our readme for all the details!")