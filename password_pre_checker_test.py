"""Module for PasswordPreChecker"""

import unittest
from password_pre_checker import PasswordPreChecker

class TestPasswordPreChecker(unittest.TestCase):
    """
    A class for testing the PasswordPreChecker class.
    """
    def setUp(self):
        """
        Set up the test fixture by initializing an instance of PasswordPreChecker
            with default values.
        """
        self.pass_checker = PasswordPreChecker()

    def test_check_length(self):
        """
        Test the check_length method of PasswordPreChecker.
        """
        self.assertTrue(self.pass_checker.check_length("password", 8))
        self.assertFalse(self.pass_checker.check_length("pass", 8))
        self.assertTrue(self.pass_checker.check_length("pass", 4))

    def test_check_contain_numbers(self):
        """
        Test the check_contain_numbers method of PasswordPreChecker.
        """
        self.assertTrue(self.pass_checker.check_contain_numbers("password1", 1))
        self.assertFalse(self.pass_checker.check_contain_numbers("password", 1))
        self.assertTrue(self.pass_checker.check_contain_numbers("pass123", 3))

    def test_check_contain_characters(self):
        """
        Test the check_contain_characters method of PasswordPreChecker.
        """
        self.assertTrue(self.pass_checker.check_contain_characters("!password", 1))
        self.assertFalse(self.pass_checker.check_contain_characters("password", 1))
        self.assertTrue(self.pass_checker.check_contain_characters("p@ssw%rd", 2))

    def test_check_size_letters(self):
        """
        Test the check_size_letters method of PasswordPreChecker.
        """
        self.assertTrue(self.pass_checker.check_size_letters("PassWord"))
        self.assertFalse(self.pass_checker.check_size_letters("password"))
        self.assertFalse(self.pass_checker.check_size_letters("PASSWORD"))

    def test_test_all_restriction(self):
        """
        Test the test_all_restriction method of PasswordPreChecker with different password cases.
        """
        self.pass_checker = PasswordPreChecker(
            char_required=8,
            num_required=1,
            spec_char_required=1
        )
        self.assertEqual(
            self.pass_checker.test_all_restriction("Pass123!"),
            [True, True, True, True]
        )
        self.assertEqual(
            self.pass_checker.test_all_restriction("Password1"),
            [True, True, False, True]
        )
        self.assertEqual(
            self.pass_checker.test_all_restriction("Password"),
            [True, False, False, True]
        )
        self.assertEqual(
            self.pass_checker.test_all_restriction("pasword"),
            [False, False, False, False]
        )
        self.assertEqual(
            self.pass_checker.test_all_restriction("pas$wor"),
            [False, False, True, False]
        )


if __name__ == '__main__':
    unittest.main()
