import unittest
from unittest.mock import patch
from decouple import config
from app import User

# Unit testing for the CLI app
# Run "python test_app.py" to run the tests
class TestApp(unittest.TestCase):

    # Set-up test data
    def setUp(self):
        self.user1 = User('test_case_user1@example.com', 'user1')
        self.user2 = User('test_case_user2@example.com', 'user2')
        self.user3 = User('test_case_user3@example.com', 'user3')

        self.user1.save()
        self.user2.save()

    # Clean-up test data
    def tearDown(self):
        self.user1.delete_user()
        self.user2.delete_user()
        self.user3.delete_user()

    def test_1_signup(self):
        """
            Checks the user creation/Sign Up functionality.
            Returns True on a successfull signup, and False on an unsuccessfull signup
        """
        self.assertEqual(self.user1.save(), False)
        self.assertEqual(self.user2.save() , False)
        self.assertEqual(self.user3.save(), True)

    def test_2_login(self):
        """
            Check the user login functionality.
            Returns True on a successfull login, and False on an invalid login
        """
        self.assertEqual(self.user1.login(), True)
        self.assertEqual(self.user2.login(), True)
        self.assertEqual(self.user3.login(), False)

    def test_3_update_user(self):
        """""
            Test the user update functionality.
            Returns True when we login with updated password, and False when we login with old password
        """""
        self.assertEqual(self.user1.update_user('user1_new'), True)
        self.assertEqual(self.user1.login(), False)
        self.user1 = User('test_case_user1@example.com', 'user1_new')
        self.assertEqual(self.user1.login(), True)

    def test_4_read_users(self):
        """""
            Test the Read all users functionality
        """""
        self.assertIn('test_case_user1@example.com', self.user1.read_users() )
        self.assertIn('test_case_user2@example.com', self.user1.read_users() )
        self.assertNotIn('test_case_user3@example.com', self.user1.read_users() )
        
    def test_5_delete_user(self):
        """""
            Test the User delete functionality.
            Returns False if we login after deleting a user, and True if we login after re-adding the user
        """""
        self.user1.delete_user()
        self.assertEqual(self.user1.login(), False)
        self.assertEqual(self.user1.save(), True)
        self.assertEqual(self.user1.login(), True)

    def test_6_weatherInfo(self):
        """
            Check the Open Weather API responses.
        """
        with patch('app.requests.get') as mocked_get:
            mocked_get.return_value.ok = True

            coordinates = self.user1.weather_info(28.7, 78.1)
            mocked_get.assert_called_with("https://api.openweathermap.org/data/2.5/onecall?lat=28.7&lon=78.1&exclude=minutely,hourly,daily,alerts&units=metric&appid=" + str(config('API_key')))
            self.assertEqual(coordinates, 'Success')

            mocked_get.return_value.ok = False

            coordinates = self.user2.weather_info(51.5, 0.1)
            mocked_get.assert_called_with("https://api.openweathermap.org/data/2.5/onecall?lat=51.5&lon=0.1&exclude=minutely,hourly,daily,alerts&units=metric&appid=" + str(config('API_key')))
            self.assertEqual(coordinates, 'Bad Response')

            
if __name__ == "__main__":
    unittest.main()