import argparse
import string
import logging
import time
import pyfiglet
from termcolor import colored
from tools.password_generator import generate_secure_password, check_password_strength
from tools.check_leaks import check_password_breach
import requests

def display_banner():
    """Display the PassHaven ASCII banner at the start of the program."""
    ascii_banner = pyfiglet.figlet_format("PassHaven", font="slant")
    print(colored(ascii_banner, "cyan"))

def display_password_info(strength: str, feedback: list[str] | None = None) -> None:
    """
    Display the password's strength and provide feedback for improvement.
    
    Args:
        strength: The password's strength rating.
        feedback: A list of suggestions for improving the password.
    """
    print(colored(f"Password Strength: {strength}", "cyan"))
    if feedback:
        print(colored("Suggestions for improvement:", "yellow"))
        for suggestion in feedback:
            print(colored(f"- {suggestion}", "yellow"))

def display_breach_warning(breached: bool, info: str) -> None:
    """
    Display a warning message indicating whether the password has been found in data breaches.
    
    Args:
        breached: Whether the password has been found in data breaches.
        info: Information about the data breach(es) containing the password.
    """
    message = f"Warning: This password has been found in {info} data breaches!" if breached else "No known breaches found."
    color = "red" if breached else "green"
    print(colored(message, color))

def generate_additional_suggestions(password: str) -> list[str]:
    """
    Generate additional suggestions for strengthening the password.
    
    Args:
        password: The password to evaluate.
    
    Returns:
        A list of suggestions for improving the password's strength.
    """
    suggestions = []

    # Check for special characters
    if not any(char in string.punctuation for char in password):
        suggestions.append("Include at least one special character, e.g., !@#$%^&*()")

    # Check password length
    if len(password) < 12:
        suggestions.append("Increase the length of the password to at least 12 characters.")

    # Check for common patterns
    common_patterns = ["password", "123", "qwerty", "letmein"]
    if any(pattern in password.lower() for pattern in common_patterns):
        suggestions.append("Avoid using common phrases or dictionary words like 'password' or '123'.")

    # Check for mixed case
    if not any(char.isupper() for char in password):
        suggestions.append("Use at least one uppercase letter.")
    if not any(char.islower() for char in password):
        suggestions.append("Use at least one lowercase letter.")

    return suggestions

def show_progress(task_name: str) -> None:
    """
    Display a simple progress indicator.

    Args:
        task_name: The name of the task being executed.
    """
    print(colored(f"{task_name}...", "blue"))
    for i in range(4):
        print(colored(f"[{'=' * i}{' ' * (3 - i)}]", "blue"), end="\r")
        time.sleep(0.5)
    print()

def main() -> None:
    """The main entry point of the program."""
    display_banner()

    logging.basicConfig(level=logging.INFO, format=colored("%(message)s", "magenta"))
    
    parser = argparse.ArgumentParser(
        description="PassHaven v1.0 - A Password Security Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('-c', '--check', help='Check if a password has been leaked in a data breach.')
    parser.add_argument('-s', '--strength', help='Check the strength of a given password.')
    parser.add_argument('-g', '--generate', action="store_true", help='Generate a strong, secure password.')
    parser.add_argument('-a', '--all', action="store_true", help='Perform all checks on the provided password.')
    parser.add_argument('--version', action='version', version='%(prog)s v0.3', help='Show the program version.')

    # Remove metavar for cleaner help message
    for action in parser._actions:
        if action.dest in ['check', 'strength']:
            action.metavar = None

    args = parser.parse_args()

    if not check_internet_connection():
        logging.error(colored("No internet connection. Please check your connection and try again.", "red"))
        return

    try:
        if args.generate:
            generate_password()
        elif args.all and args.check:
            show_progress("Checking password")
            check_password(args.check, check_breaches=True, check_strength=True)
        elif args.check:
            show_progress("Checking password")
            check_password(args.check, check_breaches=True, check_strength=False)
        elif args.strength:
            show_progress("Checking password strength") 
            check_password(args.strength, check_breaches=False, check_strength=True)
        else:
            parser.print_help()
    except Exception as e:
        logging.error(colored(f"An error occurred: {e}", "red"))

def generate_password() -> None:
    """Generate a secure password and print it with analysis."""
    logging.info(colored("Generating a secure password...", "cyan"))
    show_progress("Generating password")
    
    generated_password = generate_secure_password()
    print(colored(f"Generated Secure Password: {generated_password}", "green"))
    
    strength, feedback = check_password_strength(generated_password)
    display_password_info(strength, feedback)
    
    additional_suggestions = generate_additional_suggestions(generated_password)
    if additional_suggestions:
        print(colored("Additional Suggestions for Strengthening Your Password:", "yellow"))
        for suggestion in additional_suggestions:
            print(colored(f"- {suggestion}", "yellow"))

def check_password(password: str, check_breaches: bool = True, check_strength: bool = True) -> None:
    """
    Check the strength and optionally the breaches of a given password.
    
    Args:
        password: The password to check.
        check_breaches: Whether to check for password breaches.
        check_strength: Whether to check the password strength.
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

def check_internet_connection() -> bool:
    """Check if the internet connection is available."""
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

if __name__ == "__main__":
    main()
