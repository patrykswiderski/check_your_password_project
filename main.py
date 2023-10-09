"""Utility to check is your passwords are properly secures"""

from password_pre_checker import PasswordPreChecker
from web_leak_checker import CheckLeakToWeb


# Initialize instances of PasswordPreChecker and CheckLeakToWeb
pass_checker = PasswordPreChecker()
leak_checker = CheckLeakToWeb()

try:
    # Open the "passwords.txt" file in read mode
    with open("passwords.txt", "r", encoding="utf-8") as data:
        # Use a generator expression to read lines and strip whitespace
        password_lines = (line.strip() for line in data)

        for password in password_lines:
            # Call the test_all_restriction method to check the password
            password_restrictions = pass_checker.test_all_restriction(password)

            # Call the check_is_leaked method to check for password leaks
            # and add it to password_restrictions list
            password_restrictions.append(leak_checker.check_is_leaked(password))

            if all(password_restrictions):
                try:
                    # Attempt to open the "secure.txt" file in read and write mode
                    with open("secure.txt", "r+", encoding="utf-8") as new_data:
                        existing_passwords = new_data.read()

                        # Check if the password is not already in the file
                        if password not in existing_passwords:
                            # Write the new password to the file
                            new_data.write(f"{password}\n")

                except FileNotFoundError:
                    # The "a+" mode automatically creates the file if it doesn't exist
                    with open("secure.txt", "a", encoding="utf-8") as new_data:
                        new_data.write(f"{password}\n")

except FileNotFoundError:
    # Handle the exception when the "passwords.txt" file does not exist
    print("The file with the given name does not exist!")
