import requests
import hashlib
import getpass
from decouple import config
import argparse

# To add the --help argument to the CLI
parser=argparse.ArgumentParser(
    description=
    '''A Python CLI application \n
    Features: \n
    1. User Authentication
       --> Login, Logout
    2. User Management
       --> Create, Update, Delete and Read Users
    3. Weather Information
       --> Weather info from latitude/longitude of place''',
    epilog=""" ----- Built for the Drone Base assignment for SWE Intern. ----- """,
    formatter_class=argparse.RawTextHelpFormatter)
args=parser.parse_args()



class User:
    
    logged_in = False

    def __init__(self, email, pwd):
        self.email =  email
        self.pwd = pwd

    # Method to login the user
    def login(self):

        # Hash the enterred password
        auth = self.pwd.encode()
        auth_hash = hashlib.md5(auth).hexdigest()
        # Check if the enterred details are correct
        with open("credentials.txt", "r") as f:
            for line in f:
                stored_email, stored_pwd = line.split(":")
                parsed_pwd = stored_pwd.split('\n')[0]

                if self.email == stored_email and auth_hash == parsed_pwd:
                    self.logged_in = True
                    print("Logged In Successfully!")
                    return True
            print("Login failed! \n")
            return False

    # Method to logut the user
    def logout(self):
        self.logged_in = False
        print('Logout Successfull!')
        return True

    # Method to verify the login credentials of a user
    def authenticate(self):

        # Hash the enterred password
        auth = self.pwd.encode()
        auth_hash = hashlib.md5(auth).hexdigest()
        # Check if the enterred details are correct
        with open("credentials.txt", "r") as f:
            for line in f:
                stored_email, stored_pwd = line.split(":")
                parsed_pwd = stored_pwd.split('\n')[0]

                if self.email == stored_email and auth_hash == parsed_pwd:
                    return True
            return False


    # Equivalent to User Sign Up
    def save(self):
        # Encode password from string to byte format for hashing
        enc_pwd = self.pwd.encode()
        # Hash the above password
        hash = hashlib.md5(enc_pwd).hexdigest()

        with open("credentials.txt", "a+") as f:
            # Go to starting of file and check if email already exists in the file
            f.seek(0)
            content = f.read()
            if self.email in content:
                print('Account already exists with this E-Mail')
                return 406
            # Go to EOF and add the user data to file
            f.seek(2)
            f.write(self.email + ':')
            f.write(hash + '\n')
        print("You have registered successfully!")

    # Method to update user's password
    def update_user(self, new_pwd):
        with open("credentials.txt", "r") as f:
            replacement = ""

            for line in f:
                stored_email, stored_pwd = line.split(":")
                parsed_pwd = stored_pwd.split('\n')[0]

                if self.email == stored_email:
                    # Get the new password and hash it
                    new_auth = new_pwd.encode()
                    new_auth_hash = hashlib.md5(new_auth).hexdigest()
                    # Replace the old password hash with the new password hash
                    line = line.replace(parsed_pwd, new_auth_hash)

                replacement = replacement + line
            
        # Re-write the file with the new changes
        with open("credentials.txt", "w") as f:
            f.write(replacement)
            print('Password Updated!')
            return 200

    # Method to delete the user's account
    def delete_user(self):

        with open("credentials.txt", "r") as f:
            lines = f.readlines()
        with open("credentials.txt", "w") as f:
            for line in lines:
                if self.email not in line.strip("\n"):
                    f.write(line)
                else:
                    self.logged_in = False
                    print('Account deleted successfully!')

    # Method to display all the user's
    def read_users(self):
        users = []
    
        with open("credentials.txt", "r") as f:
            for line in f:
                stored_email = line.split(":")[0]
                users.append(stored_email)
        
        print('List of all users: \n')
        for user in users:
            print(user)

        return user

    
    def weather_info(self, lat, lon):
        API_key = config('API_key')
        
        response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + lat +"&lon=" + lon + "&exclude=minutely,hourly,daily,alerts&units=metric" + "&appid=" + API_key)
        if response.status_code != 200:
            return print('Error getting a response from the API')
        data = response.json()
        print('Weather at', lat, ',', lon, 'is: ')
        print('Humidity: ', data['current']['humidity'], "%")
        print('Pressure: ', data['current']['pressure'], "hPa")
        print('Temperature: ', data['current']['temp'], "°C")
        print('Wind Speed: ', data['current']['wind_speed'], "metre/sec")
        print('Wind Degree: ', data['current']['wind_deg'], "°")
        print('UV Index: ', data['current']['uvi'])




def main():
    USER_MANAGEMENT = False
    LOGGED_IN = False
    WEATHER_INFO = False

    # Menu-driven program
    while True:
        if LOGGED_IN == False:
            print("-------------- LOGIN SYSTEM -----------------")
            print("1. Signup")
            print("2. Login")
            print("3. Exit")
            ch = int(input("Enter your choice: "))
            
            if ch == 1:
                email = input('Enter your email: ')
                pwd = getpass.getpass('Enter your password: ')
                conf_pwd = getpass.getpass('Enter password again: ')
                if pwd == conf_pwd:
                    user = User(email, pwd)
                    user.save()
                else:
                    print('Password is not the same')

            elif ch == 2:
                email = input('Enter email: ')
                pwd = getpass.getpass('Enter password: ')
                user = User(email, pwd)
                login = user.login()
                if login:
                    LOGGED_IN = True

            elif ch == 3:
                break

            else:
                print("Wrong Choice!")
        else:
            if USER_MANAGEMENT == True:
                print("----------- USER MANAGEMENT ----------------")
                print("1. Add a new user")
                print("2. Update my password")
                print("3. Delete my account")
                print("4. Display all the users")
                print("5. Go back to dashboard")    
                ch = int(input("Enter your choice: "))

                if ch == 1:
                    email = input('Enter email: ')
                    pwd = getpass.getpass('Enter password: ')
                    conf_pwd = getpass.getpass('Enter password again: ')
                    if pwd == conf_pwd:
                        add_user = User(email, pwd)
                        add_user.save()
                    else:
                        print('Password is not the same')

                elif ch == 2:
                    pwd = getpass.getpass(prompt="Enter Old Password: ")
                    user = User(user.email, pwd)
                    if user.authenticate():
                        new_pwd = getpass.getpass(prompt="Enter New Password: ")
                        user.update_user(new_pwd)

                elif ch == 3:
                    confirmation = input('Are you sure you want to delete your account? (y/n)')
                    if confirmation == 'y' or confirmation == 'Y':
                        user.delete_user()
                        LOGGED_IN = False

                elif ch == 4:
                    user.read_users()

                elif ch == 5:
                    USER_MANAGEMENT = False

                else:
                    print("Wrong Choice!")

            elif WEATHER_INFO == True:
                print("----------- WEATHER DASHBOARD ----------------")
                print("1. Get weather information about a place")
                print("2. Go back to main menu")
                ch = int(input("Enter your choice: "))

                if ch == 1:
                    lat = input('Enter latitude of place: ')
                    lon = input('Enter longitude of place: ')
                    user.weather_info(lat, lon)

                elif ch == 2:
                    WEATHER_INFO = False
                else:

                    print("Wrong Choice!")

            else: 
                print("----------- WELCOME TO USER DASHBOARD ----------------")
                print("1. User Management")
                print("2. Weather Info")
                print("3. Logout")

                ch = int(input("Enter your choice: "))
                if ch == 1:
                    USER_MANAGEMENT = True
                elif ch == 2:
                    WEATHER_INFO = True
                elif ch == 3:
                    user = user.logged_in
                    LOGGED_IN = False
                else:
                    print("Wrong Choice!")


if __name__ == '__main__':
    main()