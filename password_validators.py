"""Checking the basic parameters of the secure text"""
from hashlib import sha1
import requests


class ValidationError(Exception):
    """Exception raised for validation errors."""

class LeakPasswordValidator:
    """A class for checking if a text has been leaked in data breaches
        using the Have I Been Pwned service.
    """

    def __init__(self):
        """Initializes a new CheckLeakWeb instance with an empty string for
            hashed text hexdigest.
        """
        self.hashed_password = ""

    def hash_text(self, text):
        """Hashes the text using SHA-1 and returns the hexadecimal digest in uppercase.

        Args:
            text (str): The text to be hashed.

        Return:
            str : The hashed text as a hexadecimal digest with upper case letters.
        """
        self.hashed_password = sha1(text.encode("utf-8")).hexdigest().upper()
        return self.hashed_password

    def get_data_hibp(self, text):
        """Retrieves data from the Have I Been Pwned service for
            the first five characters of the hashed text.

        Args:
            text (str): The text to be checked for leaks.

        Return:
            str : The response text from the Have I Been Pwned service.
        """
        first_characters = self.hash_text(text)[:5]
        response = requests.get(url=f"https://api.pwnedpasswords.com/range/{first_characters}")
        return response.text

    def is_leaked(self, text):
        """Checks if the text has been leaked in data breaches.

        Args:
            text (str): The text to be checked for leaks.

        Return:
            bool : False if the text is found in the Have I Been Pwned database, True otherwise.
        """
        rest_char_password = self.hash_text(text)[5:]
        response_hipb = self.get_data_hibp(text)
        for line in response_hipb.splitlines():
            found_hash, _ = line.split(":")
            if found_hash == rest_char_password:
                return False
        return True

class PasswordValidator(LeakPasswordValidator):
    """A class for checking the compliance of a text with specified restrictions."""
    def __init__(self, char_required=8, num_required=1, spec_char_required=1):
        """Initializes a new PasswordValidator instance with empty list for test results
            and default values for text restrictions.

        Args:
            char_required (int): Specifies the minimum number of characters in the text.
            num_required (int): Specifies the minimum number of numeric digits in the text.
            spec_char_required (int): Specifies the minimum number of non-alphanumeric characters
                in the text.
        """
        super().__init__()  # Call the parent class's __init__ method
        self.test_results = []
        self.char_required = char_required
        self.num_required = num_required
        self.spec_char_required = spec_char_required

    def is_valid(self, text):
        """Tests the text against various restrictions and accumulates the results.

        Args:
            text (str): The text to be checked.

        Return:
            bool: True if all constraints are met, False otherwise
        """
        try:
            self.length_validator(text)
            self.has_numbers_validator(text)
            self.has_characters_validator(text)
            self.different_size_validator(text)
            self.is_leaked(text)
            return True
        except ValidationError as e:
            print(e)
            return False

    def length_validator(self, text, char_required=8):
        """Checks if the text meets the minimum length requirement.

        Args:
            text (str): The text to be checked.
            char_required (ini): Specifies the minimum number of characters in the text.

        Return:
            bool : True if the condition is met.

        Raises:
            ValidationError: If the condition is not met.
        """
        if len(text) >= char_required:
            return True
        raise ValidationError(f"Text must contain minimum {char_required} characters!")

    def has_numbers_validator(self, text, num_required=1):
        """Checks if the text contains a minimum number of numeric digits.

        Args:
            text (str): The text to be checked.
            num_required (ini): Specifies the minimum number of numeric digits in the text.

        Return:
            bool : Where condition_met is True if the condition is met, False otherwise.

        Raises:
            ValidationError: If the condition is not met.
        """
        list_of_number = [True for letter in text if letter.isnumeric()]
        if len(list_of_number) >= num_required:
            return True
        raise ValidationError(f"Text must contain minimum {num_required} numbers!")

    def has_characters_validator(self, text, spec_char_required=1):
        """
        Checks if the text contains a minimum number of non-alphanumeric characters.

        Args:
            text (str): The text to be checked.
            spec_char_required (ini): Specifies the minimum number of non-alphanumeric characters in
                the text.

        Return:
            bool : True if the condition is met, False otherwise.

        Raises:
            ValidationError: If the condition is not met.
        """
        list_of_characters = [letter for letter in text if not letter.isalnum()]
        if len(list_of_characters) >= spec_char_required:
            return True
        raise ValidationError(f"Text must contain minimum {spec_char_required} special characters!")

    def different_size_validator(self, text):
        """Checks if the text contains both uppercase and lowercase letters.

        Args:
            text (str): The text to be checked.

        Return:
            bool : True if the condition is met, False otherwise.

        Raises:
            ValidationError: If the condition is not met.
        """
        list_capitalized_letters = [True for letter in text if letter.isupper()]
        list_lower_case_letters = [True for letter in text if letter.islower()]
        if any(list_capitalized_letters) and any(list_lower_case_letters):
            return True
        raise ValidationError("Text must contain both lower and upper case letters!")
