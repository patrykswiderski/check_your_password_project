"""Checking if the password has leaked to the network"""

from hashlib import sha1
import requests


HIPB_ENDPOINT = "https://api.pwnedpasswords.com/range"

class CheckLeakWeb:
    """A class for checking if a password has been leaked in data breaches
        using the Have I Been Pwned service.
    """
    def __init__(self, password):
        """Initializes a new CheckLeakWeb instance with the given password.

        Args:
            password (str): The password to be checked for leaks.
        """
        self.password = password

    def hashing_password(self):
        """Hashes the password using SHA-1 and returns the hexadecimal digest in uppercase.

        Return:
            str : The hashed password as a hexadecimal digest.
        """
        hashed_password = sha1(self.password.encode("utf-8"))
        hashed_password_hexdigest = hashed_password.hexdigest().upper()
        return hashed_password_hexdigest

    def get_data_hibp(self):
        """Retrieves data from the Have I Been Pwned service for
            the first five characters of the hashed password.

        Return:
            str : The response text from the Have I Been Pwned service.
        """
        first_characters = self.hashing_password()[0:5]
        try:
            r = requests.get(url=f"{HIPB_ENDPOINT}/{first_characters}", timeout=(5, 5))
            print(r.status_code)
            return r.text
        except requests.exceptions.Timeout:
            print("Sorry we have difficulties to get information from server. Try again later.")
            return False

    def check_is_leaked(self):
        """Checks if the password has been leaked in data breaches.

        Return:
            bool : True if the password is found in the Have I Been Pwned database, False otherwise.
        """
        rest_characters_password = self.hashing_password()[5:-1]
        if self.get_data_hibp() and rest_characters_password in self.get_data_hibp():
            print("Found!")
            return True
        else:
            print("Not found!")
            return False
