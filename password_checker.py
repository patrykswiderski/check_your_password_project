""""""
from hashlib import sha1


def check_length(word, limit=8) -> bool:
    """
    Args:
        :param limit (int): specifies the minimum number of characters in the word
        :type word (str): password to be checked

    Returns:

    """
    if len(word) >= limit:
        return True
    else:
        return False


def check_contain_numbers(word, limit=1):
    """

    :param limit: specifies the minimum number of numbers in the word
    :type word: password to be checked
    """
    list_of_number = [True for letter in word if letter.isnumeric()]
    if len(list_of_number) >= limit:
        return True, len(list_of_number)
    else:
        return False


def check_contain_characters(word, limit=1):
    """

    :param limit: specifies the minimum number of characters in the word
    :type word: password to be checked
    """
    list_of_characters = [letter for letter in word if not letter.isalnum()]
    if len(list_of_characters) >= limit:
        return True, list_of_characters
    else:
        return False


def check_size_letters(word):
    """

    :type word: password to be checked
    """
    list_capitalized_letters = [True for letter in word if letter.isupper()]
    list_lower_case_letters = [True for letter in word if letter.islower()]
    if any(list_capitalized_letters) and any(list_lower_case_letters):
        return True
    else:
        return False


# def search_database(word):
#     hashed_password = sha1(word.encode("utf-8"))
#     return hashed_password.hexdigest()[0:5]


# word_to = "1Swiderski"
# print(search_database(word=word_to))
#
# hashed_password = sha1(word_to.encode("utf-8"))
# print(hashed_password.hexdigest())
# print(hashed_password.hexdigest()[5:-1])