import argparse
import string
import logging
import time
import pyfiglet
from termcolor import colored
from password_generator import generate_secure_password, check_password_strength
from check_leaks import check_password_breach

def display_banner():
    """
    Display the PassHaven ASCII banner at the start of the program.
    """
    ascii_banner = pyfiglet.figlet_format("PassHaven", font="slant")  # You can change the font here
    print(colored(ascii_banner, "cyan"))

def display_password_info(strength, feedback=None):
    """
    Display the password's strength and provide feedback for improvement.
    
    Parameters:
    strength (str): The password's strength rating.
    feedback (list[str], optional): A list of suggestions for improving the password. Defaults to None.
    """
    print(colored(f"Password Strength: {strength}", "cyan"))
    if feedback:
        print(colored("Suggestions for improvement:", "yellow"))
        for suggestion in feedback:
            print(colored(f"- {suggestion}", "yellow"))

def display_breach_warning(breached, info):
    """
    Display a warning message indicating whether the password has been found in data breaches.
    
    Parameters:
    breached (bool): Whether the password has been found in data breaches.
    info (str): Information about the data breach(s) that contain the password.
    """
    if breached:
        print(colored(f"Warning: This password has been found in {info} data breaches!", "red"))
    else:
        print(colored("No known breaches found.", "green"))

def generate_additional_suggestions(password):
    """
    Generate additional suggestions for strengthening the password.
    
    Parameters:
    password (str): The password to evaluate.
    
    Returns:
    list[str]: A list of suggestions for improving the password's strength.
    """
    suggestions = []

    # Suggest including special characters if not already included
    if not any(char in string.punctuation for char in password):
        suggestions.append("Include at least one special character, e.g., !@#$%^&*()")

    # Suggest a longer password if less than 12 characters
    if len(password) < 12:
        suggestions.append("Increase the length of the password to at least 12 characters.")

    # Suggest avoiding dictionary words
    common_patterns = [r"password", r"123", r"qwerty", r"letmein"]
    if any(word in password.lower() for word in common_patterns):
        suggestions.append("Avoid using common phrases or dictionary words like 'password' or '123'.")

    # Suggest using mixed case
    if not any(char.isupper() for char in password):
        suggestions.append("Use at least one uppercase letter.")
    if not any(char.islower() for char in password):
        suggestions.append("Use at least one lowercase letter.")

    return suggestions

def show_progress(task_name):
    """
    Display a simple progress indicator.

    Parameters:
    task_name (str): The name of the task being executed.
    """
    print(colored(f"{task_name}...", "blue"))
    for i in range(4):
        print(colored(f"[{'=' * i}{' ' * (3 - i)}]", "blue"), end="\r")
        time.sleep(0.5)

def main():
    """
    The main entry point of the program.
    """
    # Display the PassHaven ASCII banner
    display_banner()

    logging.basicConfig(level=logging.INFO, format=colored("%(message)s", "magenta"))
    
    # Adjust the description and argument help messages for clarity
    parser = argparse.ArgumentParser(
        description="PassHaven v0.3 - A Password Security Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Define arguments and their descriptions
    parser.add_argument(
        '-c', '--check', 
        help='Check if a password has been leaked in a data breach.'
    )
    parser.add_argument(
        '-s', '--strength', 
        help='Check the strength of a given password.'
    )
    parser.add_argument(
        '-g', '--generate', 
        action="store_true", 
        help='Generate a strong, secure password.'
    )
    parser.add_argument(
        '--version', 
        action='version', 
        version='%(prog)s v0.3',  # Include version info
        help='Show the program version.'
    )

    # Remove metavar to stop using capitalized arguments in the help message
    for action in parser._actions:
        if action.dest in ['check', 'strength']:
            action.metavar = None

    args = parser.parse_args()

    try:
        if args.generate:
            generate_password()
        elif args.check:
            show_progress("Checking password")
            check_password(args.check, check_breaches=True, check_strength=False)  # Disable strength check here
        elif args.strength:
            show_progress("Checking password strength")
            check_password(args.strength, check_breaches=False, check_strength=True)  # Only strength check
        else:
            parser.print_help()
    except Exception as e:
        logging.error(colored(f"An error occurred: {e}", "red"))

def generate_password():
    """
    Generate a secure password and print it.
    """
    logging.info(colored("Generating a secure password...", "cyan"))
    show_progress("Generating password")
    generated_password = generate_secure_password()
    print(colored(f"Generated Secure Password: {generated_password}", "green"))

def check_password(password, check_breaches=True, check_strength=True):
    """
    Check the strength and optionally the breaches of a given password.
    
    Parameters:
    password (str): The password to check.
    check_breaches (bool): Whether to check for password breaches. Default is True.
    check_strength (bool): Whether to check the password strength. Default is True.
    """
    try:
        if check_strength:
            logging.info(colored("Analyzing password strength...", "cyan"))
            strength, feedback = check_password_strength(password)
            display_password_info(strength, feedback)

        if check_breaches:
            logging.info(colored("Checking for password breaches...", "cyan"))
            show_progress("Checking breaches")
            breached, info = check_password_breach(password)
            display_breach_warning(breached, info)

        additional_suggestions = generate_additional_suggestions(password)
        if additional_suggestions:
            print(colored("Additional Suggestions for Strengthening Your Password:", "yellow"))
            for suggestion in additional_suggestions:
                print(colored(f"- {suggestion}", "yellow"))

    except Exception as e:
        logging.error(colored(f"Error while processing the password: {e}", "red"))

if __name__ == "__main__":
    main()
