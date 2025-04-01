import string
import random

def generate_secure_password(length=16):
    """
    Generate a secure random password.

    Parameters:
    length (int): The length of the password to generate. Default is 16.

    Returns:
    str: A randomly generated secure password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.SystemRandom().choice(characters) for _ in range(length))

def check_password_strength(password):
    """
    Check the strength of a given password and provide feedback.

    Parameters:
    password (str): The password to evaluate.

    Returns:
    tuple: A tuple containing the strength rating and a list of feedback suggestions.
    """
    criteria = [
        (lambda s: len(s) >= 8, "Password should be at least 8 characters long."),
        (lambda s: any(char.isupper() for char in s), "Password should contain at least one uppercase letter."),
        (lambda s: any(char.islower() for char in s), "Password should contain at least one lowercase letter."),
        (lambda s: any(char.isdigit() for char in s), "Password should contain at least one digit."),
        (lambda s: any(char in string.punctuation for char in s), "Password should contain at least one special character.")
    ]

    strength_score = sum(1 for check, _ in criteria if check(password))
    feedback = [message for check, message in criteria if not check(password)]

    result = "Strong" if strength_score == 5 else "Moderate" if strength_score >= 3 else "Weak"
    return result, feedback
