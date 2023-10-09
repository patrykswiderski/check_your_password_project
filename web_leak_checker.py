""""""
from hashlib import sha1
import requests


HIPB_ENDPOINT = "https://api.pwnedpasswords.com/range"
""""""
class CheckLeakWeb:

    def __init__(self, password):
        self.password = password

    def hashing_password(self):
        hashed_password = sha1(self.password.encode("utf-8"))
        hashed_password_hexdigest = hashed_password.hexdigest().upper()
        return hashed_password_hexdigest

    def get_data_hibp(self):
        first_characters = self.hashing_password()[0:5]
        try:
            r = requests.get(url=f"{HIPB_ENDPOINT}/{first_characters}", timeout=(5, 5))
            print(r.status_code)
            return r.text
        except requests.exceptions.Timeout:
            print("Sorry we have difficulties to get information from server. Try again later.")
            return False

    def check_is_leaked(self):
        rest_characters_password = self.hashing_password()[5:-1]
        try:
            if self.get_data_hibp and rest_characters_password in self.get_data_hibp:
                print("Found!")
                return True
            else:
                print("Not found!")
                return False
        except TypeError:
            print("Sorry we have difficulties to get information from haveibeenpwned.com.\n"
                  "Try again later.")
            return False


# word_to = "2001avensistoyota1234"
# c = CheckLeakWeb(password=word_to)
# c.get_data_hibp()







