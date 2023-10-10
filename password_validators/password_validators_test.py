"""Module for test PasswordValidator"""

import unittest
from unittest.mock import patch
from io import StringIO
import pytest
from password_validators import PasswordValidator, ValidationError, LeakPasswordValidator

class TestPasswordValidator(unittest.TestCase):
    """
    A class for testing the PasswordValidator class.
    """
    def setUp(self):
        """
        Set up the test fixture by initializing an instance of PasswordValidator
            with default values.
        """
        self.validator = PasswordValidator(
            char_required=8,
            num_required=1,
            spec_char_required=1
        )

    def test_length_validator(self):
        """
        Test the check_length method of PasswordValidator.
        """
        self.assertTrue(self.validator.length_validator("password", char_required=8))
        with pytest.raises(ValidationError) as error:
            self.validator.length_validator("pass", 8)
            self.assertEqual(
                str(error.value),
                "Text must contain minimum 8 characters!"
            )
        self.assertTrue(self.validator.length_validator("pass", char_required=4))

    def test_has_numbers_validator(self):
        """
        Test the check_contain_numbers method of PasswordValidator.
        """
        self.assertTrue(self.validator.has_numbers_validator("passw1ord", num_required=1))
        with pytest.raises(ValidationError) as error:
            self.validator.has_numbers_validator("text", num_required=1)
            self.assertEqual(
                str(error.value),
                "Text must contain minimum 1 numbers!"
            )
        self.assertTrue(self.validator.has_numbers_validator("pass123", num_required=3))

    def test_has_characters_validator(self):
        """
        Test the check_contain_characters method of PasswordValidator.
        """
        self.assertTrue(self.validator.has_characters_validator("!text", spec_char_required=1))
        with pytest.raises(ValidationError) as error:
            self.validator.has_characters_validator("text", spec_char_required=1)
            self.assertEqual(
                str(error.value),
                "Text must contain minimum 1 special characters!"
            )
        self.assertTrue(self.validator.has_characters_validator("p@ssw%rd", spec_char_required=2))

    def test_different_size_validator(self):
        """
        Test the check_size_letters method of PasswordValidator.
        """
        self.assertTrue(self.validator.different_size_validator("PassWord"))
        with pytest.raises(ValidationError) as error:
            self.validator.different_size_validator("text")
            self.assertEqual(
                str(error.value),
                "Text must contain lower and upper letters!"
            )
        with pytest.raises(ValidationError) as error:
            self.validator.different_size_validator("PASSWORD")
            self.assertEqual(
                str(error.value),
                "Text must contain lower and upper letters!"
            )

    def test_is_valid(self):
        """
        Test the test all restriction method of PasswordValidator with different text cases.
        """

        self.assertEqual(
            self.validator.is_valid("pas$wor"),
            False
        )

        self.assertEqual(
            self.validator.is_valid("Pass123!"),
            True
        )

class TestCheckLeakToWeb(unittest.TestCase):
    """
    A class for testing the LeakPasswordValidator class.
    """

    def setUp(self):
        """
        Set up the test fixture by initializing an instance of LeakPasswordValidator.
        """
        self.leak_checker = LeakPasswordValidator()

    def test_hashing_password(self):
        """
        Test the hash_text method of LeakPasswordValidator.
        """
        hashed_password = self.leak_checker.hash_text("password123")
        self.assertEqual(hashed_password, "CBFDAC6008F9CAB4083784CBD1874F76618D2A97")

    @patch('requests.get')
    def test_get_data_hibp(self, mock_requests_get):
        """
        Test the get_data_hibp method of LeakPasswordValidator with mock requests.get.
        """
        mock_response = StringIO(
            "D4919A1D2ACFB4FFDB48FF31947B13A9515:1\n"
            "D4BF244F0936E450388DBF3BFC59FBC23CF:1\n"
            "D4FCD8FCD0812F85468023DC90F4B09D45F:4"
        )
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.text = mock_response.read()

        response = self.leak_checker.get_data_hibp("password123")
        self.assertEqual(
            response,
            "D4919A1D2ACFB4FFDB48FF31947B13A9515:1\n"
            "D4BF244F0936E450388DBF3BFC59FBC23CF:1\n"
            "D4FCD8FCD0812F85468023DC90F4B09D45F:4"
        )

    def test_check_is_leaked(self):
        """
        Test the check_is_leaked method of LeakPasswordValidator.
        """
        with patch('requests.get') as mock_requests_get:
            mock_response = StringIO(
            "C6008F9CAB4083784CBD1874F76618D2A97:1\n"
            "D4BF244F0936E450388DBF3BFC59FBC23CF:1\n"
            "D4FCD8FCD0812F85468023DC90F4B09D45F:4"
        )
            mock_requests_get.return_value.status_code = 200
            mock_requests_get.return_value.text = mock_response.read()

            self.assertFalse(self.leak_checker.is_leaked("password123"))
            self.assertTrue(self.leak_checker.is_leaked("securepassword"))

if __name__ == '__main__':
    unittest.main()
