import unittest
import app

# Unit testing for the CLI app
# Run "python test_app.py" to run the tests
class TestApp(unittest.TestCase):

    def test_1_signup(self):
        """""
            User creation/Sign Up functionality
        """""
        self.assertEqual(app.signup('test_case@example.com', 'test', 'test123'), 409)
        self.assertEqual(app.signup('test_case@example.com', 'test', 'test'), 200)
        self.assertEqual(app.signup('test_case@example.com', 'test', 'test'), 406)

    def test_2_login(self):
        """""
            User Login functionality
        """""
        self.assertEqual(app.login('test_case@example.com', 'test456'), 403)
        self.assertEqual(app.login('test_case@example.com', 'test'), 200)

    def test_3_update_user(self):
        """""
            User update functionality
        """""
        self.assertEqual(app.update_user('test_case@example.com', 'test789', 'test_new'), 403)
        self.assertEqual(app.update_user('test_case@example.com', 'test', 'test_new'), 200)

    def test_4_read_users(self):
        """""
            Read all users functionality
        """""
        self.assertEqual(app.read_users(), 'test_case@example.com')
        
    def test_5_delete_user(self):
        """""
            User delete functionality
        """""
        self.assertEqual(app.delete_user('invalid_test_case@example.com'), 404)
        self.assertEqual(app.delete_user('test_case@example.com'), 200)



if __name__ == "__main__":
    unittest.main()