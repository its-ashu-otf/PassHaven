import string
import random
import logging
import secrets  # Added for better randomness

def generate_secure_password(length=16, include_spaces=False):
    """
    Generate a secure random password.

    Parameters:
    length (int): The length of the password to generate. Default is 16.
    include_spaces (bool): Whether to include spaces in the password. Default is False.

    Returns:
    str: A randomly generated secure password.
    """
    if length < 8:
        logging.warning("Requested password length is less than the recommended minimum of 8 characters.")
        length = 16  # Default to 16 if a lower length is provided

    characters = string.ascii_letters + string.digits + string.punctuation
    if include_spaces:
        characters += ' '  # Include space if specified

    password = ''.join(secrets.choice(characters) for _ in range(length))  # Use secrets for better randomness
    logging.info(f"Generated password of length {length}.")
    return password

def check_password_strength(password):
    """
    Check the strength of a given password and provide feedback.

    Parameters:
    password (str): The password to evaluate.

    Returns:
    tuple: A tuple containing the strength rating and a list of feedback suggestions.
    """
    if not isinstance(password, str):
        logging.error("Password must be a string.")
        raise ValueError("Password must be a string.")

    if len(password) == 0:
        logging.error("Password cannot be empty.")
        raise ValueError("Password cannot be empty.")

    criteria = [
        (lambda s: len(s) >= 8, "Password should be at least 8 characters long."),
        (lambda s: any(char.isupper() for char in s), "Password should contain at least one uppercase letter."),
        (lambda s: any(char.islower() for char in s), "Password should contain at least one lowercase letter."),
        (lambda s: any(char.isdigit() for char in s), "Password should contain at least one digit."),
        (lambda s: any(char in string.punctuation for char in s), "Password should contain at least one special character."),
        (lambda s: len(set(s)) >= 10, "Password should have at least 10 unique characters.")  # New criterion
    ]

    strength_score = sum(1 for check, _ in criteria if check(password))
    feedback = [message for check, message in criteria if not check(password)]

    result = "Strong" if strength_score == 6 else "Moderate" if strength_score >= 4 else "Weak"  # Updated for new criterion
    logging.info(f"Password strength evaluated: {result}.")
    return result, feedback
