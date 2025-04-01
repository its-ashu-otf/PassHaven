import requests
import hashlib
import socket

def check_internet_connection():
    """Check if the internet connection is available."""
    try:
        # Try to connect to a well-known host
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

def check_password_breach(password):
    """
    Check if the password has been breached using Pwned Passwords API.

    Parameters:
    password (str): The password to check.

    Returns:
    tuple: A tuple containing a boolean indicating if the password was breached and a message or breach count.
    """
    if not check_internet_connection():
        return False, "No internet connection. Please check your connection and try again."

    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return False, f"Error checking password breach status: {e}"

    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return True, count.strip()

    return False, "Password not found in breach databases."
