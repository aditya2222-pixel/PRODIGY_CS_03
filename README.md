# Password Complexity & Breach Checker

## Task 03 - Prodigy InfoTech Cyber Security Internship

A Python GUI application that evaluates password strength based on multiple complexity criteria and checks whether a password appears in known data breaches using the Have I Been Pwned (HIBP) API.

## Features

- Real-time password strength evaluation
- Checks password length
- Checks for uppercase letters
- Checks for lowercase letters
- Checks for numbers
- Checks for special characters
- Displays Weak, Moderate, or Strong strength status
- Password visibility toggle
- Checks passwords against known data breaches
- Uses SHA-1 hashing with the HIBP k-anonymity API
- Generates a random 16-character password
- Uses a system-based secure random generator
- Simple graphical user interface using Tkinter

## Technologies Used

- Python
- Tkinter
- hashlib
- urllib
- string
- random
- Have I Been Pwned (HIBP) API

## How It Works

The application evaluates a password using five basic criteria:

1. At least 8 characters
2. At least one uppercase letter
3. At least one lowercase letter
4. At least one number
5. At least one special character

The application updates the strength indicator in real time as the user enters the password.

### Strength Levels

| Criteria Met | Strength |
|---|---|
| 0–2 | Weak |
| 3–4 | Moderate |
| 5 | Strong |

## HIBP Breach Check

The application uses the Have I Been Pwned (HIBP) Passwords API to check whether a password has appeared in known data breaches.

For privacy, the complete password is not sent to the API.

The application:

1. Creates a SHA-1 hash of the password locally.
2. Splits the hash into a 5-character prefix and remaining suffix.
3. Sends only the first 5 characters to the HIBP API.
4. Receives matching hash suffixes.
5. Compares the suffix locally.
6. Displays whether a matching breach record was found.

This approach uses the HIBP k-anonymity model.

## Password Generator

The application includes a password generator that creates a 16-character password using:

- Uppercase letters
- Lowercase letters
- Numbers
- Special characters

The generator uses Python's `SystemRandom` to obtain randomness from the operating system.

## User Interface

The application provides:

- Password input field
- Password visibility toggle
- Real-time strength indicator
- Complexity criteria checklist
- HIBP breach status
- Check Password button
- Generate Password button
- Suggested Password field

## How to Run

### 1. Install Python

Make sure Python 3 is installed on your system.

Check your Python installation:

```bash
python --version
```

### 2. Run the Application

Open a terminal in the project folder and run:

```bash
python main.py
```

## Internet Requirement

An internet connection is required for the HIBP breach-checking feature.

The following features work locally:

- Password strength evaluation
- Complexity checking
- Password generation
- Password visibility toggle

## Project Structure

```text
PRODIGY_CS_03/
│
├── main.py
├── README.md
├── .gitignore
│
└── screenshots/
    └── screenshot.png
```

## Screenshot

### Password Complexity & Breach Checker

![Password Complexity & Breach Checker](screenshots/screenshot.png)

## Task

This project was completed as part of the Prodigy InfoTech Cyber Security Internship.

**Task:** Build a tool that assesses the strength of a password based on criteria such as length, presence of uppercase and lowercase letters, numbers, and special characters, and provides feedback on the password's strength.

## Disclaimer

This project was developed for educational purposes as part of a cybersecurity internship.

The breach-checking feature uses the Have I Been Pwned Passwords API and does not send the complete password to the API.
