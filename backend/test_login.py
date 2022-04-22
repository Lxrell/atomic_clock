import unittest

from login import Login

class LoginTest(unittest.TestCase):

    def test_get_time_from_server_with_response():
        pass

    def test_get_time_from_server_without_response():
        pass

    def test_connect_to_database():
        pass

    def test_get_cursor():
        pass

    def test_table_exists_returns_true_with_existing_table():
        pass

    def test_table_exists_returns_false_without_existing_table():
        pass

    def test_create_table():
        pass

    def test_populate_table_adds_credentials():
        pass

    def test_populate_table_saves_credentials():
        pass

    def test_get_last_login_date_on_first_login():
        pass

    def test_get_last_login_date_on_subsequent_login():
        pass

    def test_set_last_login_date():
        pass

    def test_login_attempt_with_valid_username_and_password():
        pass

    def test_login_attempt_with_invalid_username():
        pass

    def test_login_attempt_with_valid_username_invalid_password():
        pass

if __name__ == "__main__":
    # Runs the tests and outputs results:
    unittest.main()