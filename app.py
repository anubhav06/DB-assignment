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


def signup(email, pwd, conf_pwd):
    if email is None and pwd is None and conf_pwd is None:
        email = input("Enter email address: ")
        pwd = getpass.getpass(prompt="Enter password: ")
        conf_pwd = getpass.getpass(prompt="Re-Enter password: ")

    if conf_pwd == pwd:
        # Encode password from string to byte format for hashing
        enc_pwd = conf_pwd.encode()
        # Hash the above password
        hash = hashlib.md5(enc_pwd).hexdigest()

        with open("credentials.txt", "a+") as f:
            # Go to starting of file and check if email already exists in the file
            f.seek(0)
            content = f.read()

            if email in content:
                print('Account already exists with this E-Mail')
                return 406

            # Go to EOF and add the user data to file
            f.seek(2)
            f.write(email + ':')
            f.write(hash + '\n')
        print("You have registered successfully!")
        return 200
    else:
        print("Password is not the same!")
        return 409

    
def login(email, pwd):
    if email is None and pwd is None: 
        email = input("Enter email: ")
        pwd = getpass.getpass(prompt="Enter password: ")
    
    # Encode password and then hash it.
    auth = pwd.encode()
    auth_hash = hashlib.md5(auth).hexdigest()

    with open("credentials.txt", "r") as f:
        for line in f:
            stored_email, stored_pwd = line.split(":")
            parsed_pwd = stored_pwd.split('\n')[0]

            if email == stored_email and auth_hash == parsed_pwd:
                global LOGGED_IN
                LOGGED_IN = True
                print("Logged In Successfully!")
                return 200

        print("Login failed! \n")
        return 403


def logout():
    global LOGGED_IN
    LOGGED_IN = False
    print('Logout Completed')


# To update a user's password
def update_user(email, pwd, new_pwd):
    
    if email is None and pwd is None:
        email = input("Enter user's email to update their password: ")
        pwd = getpass.getpass(prompt="Enter Old Password: ")
    # Encode password and then hash it.
    auth = pwd.encode()
    auth_hash = hashlib.md5(auth).hexdigest()

    
    with open("credentials.txt", "r") as f:
        replacement = ""
        valid_credentials = False

        for line in f:
            stored_email, stored_pwd = line.split(":")
            parsed_pwd = stored_pwd.split('\n')[0]

            if email == stored_email and auth_hash == parsed_pwd:
                valid_credentials = True
                # Get the new password and hash it
                if new_pwd is None:
                    new_pwd = getpass.getpass(prompt="Enter New Password: ")
                new_auth = new_pwd.encode()
                new_auth_hash = hashlib.md5(new_auth).hexdigest()
                # Replace the old password hash with the new password hash
                line = line.replace(parsed_pwd, new_auth_hash)

            replacement = replacement + line
        
        if valid_credentials == False:
            print("Incorrect Password! \n")
            return 403

    # Re-write the file with the new changes
    with open("credentials.txt", "w") as f:
        f.write(replacement)
        print('Password Updated!')
        return 200


# To delete a user's account
def delete_user(email):

    user_found = False
    if email is None:
        email = input("Enter user's email whose account is to be deleted: ")

    with open("credentials.txt", "r") as f:
        lines = f.readlines()
    with open("credentials.txt", "w") as f:
        for line in lines:
            if email not in line.strip("\n"):
                f.write(line)
            else:
                user_found = True
    
    if user_found == True:
        print("User:'",email,"'deleted successfully !")
        return 200
    else:
        print('No account found with that email !')
        return 404


# To display all the user's
def read_users():
    users = []
    
    with open("credentials.txt", "r") as f:
        for line in f:
            stored_email = line.split(":")[0]
            users.append(stored_email)
    
    print('List of all users: \n')
    for user in users:
        print(user)

    return user


def weather_info():
    lat = input('Enter latitude of place: ')
    lon = input('Enter lomgitude of place: ')
    API_key = config('API_key')
    
    response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + lat +"&lon=" + lon + "&exclude=minutely,hourly,daily,alerts&units=metric" + "&appid=" + API_key)
    if response.status_code != 200:
        return print('Error getting a response from the API')
    data = response.json()
    print('Humidity: ', data['current']['humidity'], "%")
    print('Pressure: ', data['current']['pressure'], "hPa")
    print('Temperature: ', data['current']['temp'], "°C")
    print('Wind Speed: ', data['current']['wind_speed'], "metre/sec")
    print('Wind Degree: ', data['current']['wind_deg'], "°")
    print('UV Index: ', data['current']['uvi'])


def main():
    # Global variable which decides if user is logged in or not
    global LOGGED_IN
    LOGGED_IN = False
    global USER_MANAGEMENT
    USER_MANAGEMENT = False
    global WEATHER_INFO
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
                signup(None, None, None)
            elif ch == 2:
                login(None, None)
            elif ch == 3:
                break
            else:
                print("Wrong Choice!")
        else:
            if USER_MANAGEMENT == True:
                print("----------- USER MANAGEMENT ----------------")
                print("1. Create a new user")
                print("2. Update a user's password")
                print("3. Delete an existing user")
                print("4. Display all the user's")
                print("5. Go back to dashboard")
                    
                ch = int(input("Enter your choice: "))
                if ch == 1:
                    signup(None, None, None)
                elif ch == 2:
                    update_user(None, None, None)
                elif ch == 3:
                    delete_user(None)
                elif ch == 4:
                    read_users()
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
                    weather_info()
                elif ch == 2:
                    WEATHER_INFO = False
                else:
                    print("Wrong Choice!")
            
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
                logout()
            else:
                print("Wrong Choice!")


if __name__ == '__main__':
    main()