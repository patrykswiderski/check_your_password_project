"""Module for test CheckLeakToWeb"""

import unittest
from unittest.mock import patch
from io import StringIO
import requests
from web_leak_checker import CheckLeakToWeb

class TestCheckLeakToWeb(unittest.TestCase):
    """
    A class for testing the CheckLeakToWeb class.
    """

    def setUp(self):
        """
        Set up the test fixture by initializing an instance of CheckLeakToWeb.
        """
        self.leak_checker = CheckLeakToWeb()

    def test_hashing_password(self):
        """
        Test the hashing_password method of CheckLeakToWeb.
        """
        hashed_password = self.leak_checker.hashing_password("password123")
        self.assertEqual(hashed_password, "CBFDAC6008F9CAB4083784CBD1874F76618D2A97")

    @patch('requests.get')
    def test_get_data_hibp(self, mock_requests_get):
        """
        Test the get_data_hibp method of CheckLeakToWeb with mock requests.get.
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

    @patch('requests.get', side_effect=requests.exceptions.Timeout)
    def test_get_data_hibp_timeout(self, _):
        """
        Test the get_data_hibp method of CheckLeakToWeb when requests.get times out.
        """
        response = self.leak_checker.get_data_hibp("password123")
        self.assertNotEqual(response, True)

    def test_check_is_leaked(self):
        """
        Test the check_is_leaked method of CheckLeakToWeb.
        """
        with patch('requests.get') as mock_requests_get:
            mock_response = StringIO(
            "C6008F9CAB4083784CBD1874F76618D2A95:1\n"
            "D4BF244F0936E450388DBF3BFC59FBC23CF:1\n"
            "D4FCD8FCD0812F85468023DC90F4B09D45F:4"
        )
            mock_requests_get.return_value.status_code = 200
            mock_requests_get.return_value.text = mock_response.read()

            self.assertFalse(self.leak_checker.check_is_leaked("password123"))
            self.assertTrue(self.leak_checker.check_is_leaked("securepassword"))

if __name__ == '__main__':
    unittest.main()
