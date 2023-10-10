"""Utility to check is your passwords are properly secured"""

from password_validators import PasswordValidator, LeakPasswordValidator


# Initialize instances of PasswordValidator and LeakPasswordValidator
pass_validator = PasswordValidator()
leak_validator = LeakPasswordValidator()

try:
    # Open the "passwords.txt" file in read mode
    with open("passwords.txt", "r", encoding="utf-8") as data:
        # Use a generator expression to read lines and strip whitespace
        password_lines = (line.strip() for line in data)
        for password in password_lines:
            # Check if the password meets the criteria and is not leaked
            if pass_validator.is_valid(password):
                try:
                    # Attempt to open the "secure.txt" file in read and write mode
                    with open("secure.txt", "r+", encoding="utf-8") as new_data:
                        existing_passwords = new_data.read()
                        # Check if the text is not already in the file
                        if password not in existing_passwords:
                            # Write the new text to the file
                            new_data.write(f"{password}\n")

                except FileNotFoundError:
                    # The "a+" mode automatically creates the file if it doesn't exist
                    with open("secure.txt", "a", encoding="utf-8") as new_data:
                        new_data.write(f"{password}\n")

except FileNotFoundError:
    # Handle the exception when the "passwords.txt" file does not exist
    print("The file with the given name does not exist!")
