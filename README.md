## Overview

PassHaven is a powerful tool designed to enhance the security of your online accounts by integrating robust password generation with advanced breach detection capabilities. This tool ensures that your passwords are not only strong but also have not been compromised in any known data breaches. With PassHaven, you can take control of your online security and protect your sensitive information effectively.


![Screencast From 2024-12-12 23-24-12](https://github.com/user-attachments/assets/b8d25929-841c-4649-822b-aef747347aa3)


## Features

- **Secure Password Generation**: Create strong, random passwords with customizable lengths to suit your needs. Choose to include special characters, numbers, and even spaces for added complexity.
- **Password Strength Evaluation**: Assess the strength of your passwords and receive actionable feedback for improvement. Get insights on how to enhance your password's security based on various criteria.
- **Breach Detection**: Check if your passwords have been exposed in any known data breaches using the Pwned Passwords API. Stay informed about potential risks to your accounts.
- **User-Friendly Interface**: Enjoy a simple and intuitive command-line interface with clear instructions and helpful feedback. Easily navigate through options to generate passwords, check strength, or verify breaches.
- **Additional Suggestions**: Receive tailored suggestions for strengthening your passwords based on common vulnerabilities and best practices.
- **Progress Indicators**: Visual feedback during operations to keep you informed about ongoing processes, such as password generation and breach checks.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PassHaven.git
   cd PassHaven
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Building 

   ```bash
   pyinstaller --onefile --hidden-import=pyfiglet --hidden-import=termcolor --hidden-import=requests --name PassHaven passhaven.py
   ```
