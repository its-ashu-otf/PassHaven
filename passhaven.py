from password_generator import generate_secure_password, check_password_strength
from check_leaks import check_password_breach
import string

def display_password_strength(strength, feedback):
    """Displays the password strength and improvement suggestions."""
    print(f"\nPassword Strength: {strength}")
    if feedback:
        print("Suggestions for improvement:")
        for suggestion in feedback:
            print(f"- {suggestion}")

def display_breach_warning(breached, info):
    """Displays breach warning if the password is found in known breaches."""
    if breached:
        print(f"\nWarning: This password has been found in {info} data breaches!")
    else:
        print(f"\nGood news! This password has not been found in any known breaches.")

def get_password_input():
    """Prompts the user to enter a password for checking."""
    password = input("Enter the password to check: ").strip()
    return password

def generate_additional_suggestions(password):
    """Generates additional suggestions to make the password stronger."""
    suggestions = []

    # Suggest including special characters if not already included
    if not any(char in string.punctuation for char in password):
        suggestions.append("Include at least one special character, e.g., !@#$%^&*()")
    
    # Suggest a longer password if less than 12 characters
    if len(password) < 12:
        suggestions.append("Increase the length of the password to at least 12 characters.")
    
    # Suggest avoiding dictionary words
    if any(word in password.lower() for word in ["password", "123", "qwerty", "letmein"]):
        suggestions.append("Avoid using common phrases or dictionary words like 'password' or '123'.")
    
    # Suggest using mixed case
    if not any(char.isupper() for char in password):
        suggestions.append("Use at least one uppercase letter.")
    if not any(char.islower() for char in password):
        suggestions.append("Use at least one lowercase letter.")

    return suggestions

def main():
    print("Welcome to PassHaven - Your Secure Password Tool!")
    choice = input("Enter '1' to check a password, '2' to generate a secure password: ").strip()

    if choice == '1':
        password = get_password_input()
        strength, feedback = check_password_strength(password)
        breached, info = check_password_breach(password)

        # Display password strength and improvement suggestions
        display_password_strength(strength, feedback)
        # Display additional suggestions for stronger password
        additional_suggestions = generate_additional_suggestions(password)
        if additional_suggestions:
            print("Additional Suggestions for Strengthening Your Password:")
            for suggestion in additional_suggestions:
                print(f"- {suggestion}")
        # Display breach warning if applicable
        display_breach_warning(breached, info)

    elif choice == '2':
        generated_password = generate_secure_password()
        print(f"\nGenerated Secure Password: {generated_password}")
    else:
        print("Invalid choice! Please enter '1' or '2'.")

if __name__ == "__main__":
    main()
