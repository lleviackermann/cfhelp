# ANSI escape codes for colors
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'

class TextFormatting:
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

def display_success_message(msg):
    print(f"{Colors.GREEN}{msg}{Colors.RESET}")
    
def display_error_message(msg):
    print(f"{Colors.RED}{msg}{Colors.RESET}")
    
def display_processing_message(msg):
    print(f"{Colors.CYAN}{msg}{Colors.RESET}")

def display_information(starting_text, middle_text, end_text="", bold=True, italic=True):
    formatted_middle_text = middle_text
    if bold:
        formatted_middle_text = f"{TextFormatting.BOLD}{formatted_middle_text}"
    if italic:
        formatted_middle_text = f"{TextFormatting.ITALIC}{formatted_middle_text}"

    formatted_starting_text = f"{Colors.CYAN}{starting_text}{Colors.RESET}"
    formatted_middle_text = f"{Colors.GREEN}{formatted_middle_text}{Colors.RESET}"
    formatted_end_text = f"{Colors.CYAN}{end_text}{Colors.RESET}"

    print(formatted_starting_text, formatted_middle_text, formatted_end_text)
    
def display_negative_information(starting_text, middle_text, end_text="", bold=True, italic=True):
    formatted_middle_text = middle_text
    if bold:
        formatted_middle_text = f"{TextFormatting.BOLD}{formatted_middle_text}"
    if italic:
        formatted_middle_text = f"{TextFormatting.ITALIC}{formatted_middle_text}"

    formatted_starting_text = f"{Colors.CYAN}{starting_text}{Colors.RESET}"
    formatted_middle_text = f"{Colors.RED}{formatted_middle_text}{Colors.RESET}"
    formatted_end_text = f"{Colors.CYAN}{end_text}{Colors.RESET}"

    print(formatted_starting_text, formatted_middle_text, formatted_end_text)    
def display_purple_text(msg):
    print(f"{Colors.PURPLE}{msg}{Colors.RESET}")