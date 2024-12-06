import string, random

# Generate a secure random password
def generate_secure_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Check password strength
def check_password_strength(password):
    strength_score = 0
    feedback = []

    if len(password) >= 8:
        strength_score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    if any(char.isupper() for char in password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")

    if any(char.islower() for char in password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")

    if any(char.isdigit() for char in password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one digit.")

    if any(char in string.punctuation for char in password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one special character.")

    result = "Strong" if strength_score == 5 else "Moderate" if strength_score >= 3 else "Weak"
    return result, feedback
