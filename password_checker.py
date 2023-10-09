"""Checking the basic parameters of the secure password"""
class PasswordPreChecker:
    """A class for checking the compliance of a password with specified restrictions.
    """
    def __init__(self):
        """Initializes a new PasswordPreChecker instance with an empty list for test results.
        """
        self.test_results = []

    def test_all_restriction(self, password, char_required=8, num_required=1, spec_char_required=1):
        """Tests the password against various restrictions and accumulates the results.

        Args:
            password (str): The password to be checked.
            char_required (ini): Specifies the minimum number of characters in the password.
            num_required (ini): Specifies the minimum number of numeric digits in the password.
            spec_char_required (ini): Specifies the minimum number of non-alphanumeric characters
                in the password.

        Return:
            list  : A list of test results, where each result is a boolean.
                condition_met is True if the condition is met, False otherwise.
        """
        self.test_results.append(self.check_length(password, char_required))
        self.test_results.append(self.check_contain_numbers(password, num_required))
        self.test_results.append(self.check_contain_characters(password, spec_char_required))
        self.test_results.append(self.check_size_letters(password))
        return self.test_results

    def check_length(self, word, limit=8) -> bool:
        """Checks if the password meets the minimum length requirement.

        Args:
            password (str): The password to be checked.
            limit (ini): Specifies the minimum number of characters in the password.

        Return:
            bool : Where condition_met is True if the condition is met, False otherwise.
        """
        if len(word) >= limit:
            return True
        else:
            return False


    def check_contain_numbers(self, password, limit=1):
        """Checks if the password contains a minimum number of numeric digits.

        Args:
            password (str): The password to be checked.
            limit (ini): Specifies the minimum number of numeric digits in the password.

        Return:
            bool : Where condition_met is True if the condition is met, False otherwise.
        """
        list_of_number = [True for letter in password if letter.isnumeric()]
        if len(list_of_number) >= limit:
            return True
        else:
            return False


    def check_contain_characters(self, password, limit=1):
        """
        Checks if the password contains a minimum number of non-alphanumeric characters.

        Args:
            password (str): The password to be checked.
            limit (ini): Specifies the minimum number of non-alphanumeric characters in
                the password.

        Return:
            bool : Where condition_met is True if the condition is met, False otherwise.
        """
        list_of_characters = [letter for letter in password if not letter.isalnum()]
        if len(list_of_characters) >= limit:
            return True
        else:
            return False


    def check_size_letters(self, password):
        """Checks if the password contains both uppercase and lowercase letters.

        Args:
            password (str): The password to be checked.

        Return:
            bool : Where condition_met is True if the condition is met, False otherwise.
        """
        list_capitalized_letters = [True for letter in password if letter.isupper()]
        list_lower_case_letters = [True for letter in password if letter.islower()]
        if any(list_capitalized_letters) and any(list_lower_case_letters):
            return True
        else:
            return False
