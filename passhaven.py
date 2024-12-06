from password_generator import generate_secure_password, check_password_strength
from check_leaks import check_password_breach

# Main function
def main():
    print("Welcome to the Secure Password Tool!")
    choice = input("Enter '1' to check a password,'2' to generate a secure password: ").strip().upper()

    if choice == '1':
        password = input("Enter the password to check: ").strip()
        strength, feedback = check_password_strength(password)
        breached, info = check_password_breach(password)

        print(f"\nPassword Strength: {strength}")
        if feedback:
            print("Suggestions for improvement:")
            for suggestion in feedback:
                print(f"- {suggestion}")

        if breached:
            print(f"\nWarning: This password has been found in {info} data breaches!")
    elif choice == '2':
        generated_password = generate_secure_password()
        print(f"\nGenerated Secure Password: {generated_password}")
    else:
        print("Invalid choice! Please enter '1' or '2'.")

if __name__ == "__main__":
    main()
