"""Checking if the password has leaked to the network"""

from hashlib import sha1
import requests


HIPB_ENDPOINT = "https://api.pwnedpasswords.com/range"

class CheckLeakToWeb:
    """A class for checking if a password has been leaked in data breaches
        using the Have I Been Pwned service.
    """
    def __init__(self):
        """Initializes a new CheckLeakWeb instance with an empty string for
            hashed password hexdigest.
        """
        self.hashed_password_hexdigest = ""

    def hashing_password(self, password):
        """Hashes the password using SHA-1 and returns the hexadecimal digest in uppercase.

        Args:
            password (str): The password to be hashed.

        Return:
            str : The hashed password as a hexadecimal digest.
        """
        hashed_password = sha1(password.encode("utf-8"))
        self.hashed_password_hexdigest = hashed_password.hexdigest().upper()
        return self.hashed_password_hexdigest

    def get_data_hibp(self, password):
        """Retrieves data from the Have I Been Pwned service for
            the first five characters of the hashed password.

        Args:
            password (str): The password to be checked for leaks.

        Return:
            str : The response text from the Have I Been Pwned service.
        """
        first_characters = self.hashing_password(password)[0:5]
        try:
            r = requests.get(url=f"{HIPB_ENDPOINT}/{first_characters}", timeout=(5, 5))
            r.status_code
            return r.text
        except requests.exceptions.Timeout:
            print("Sorry we have difficulties to get information from server. Try again later.")
            return False

    def check_is_leaked(self, password):
        """Checks if the password has been leaked in data breaches.

        Args:
            password (str): The password to be checked for leaks.

        Return:
            bool : True if the password is found in the Have I Been Pwned database, False otherwise.
        """
        rest_char_password = self.hashing_password(password)[5:-1]
        if self.get_data_hibp(password) and rest_char_password in self.get_data_hibp(password):
            print("Found!")
            return False
        else:
            print("Not found!")
            return True
