import hashlib
import getpass

def signup():
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
                return

            # Go to EOF and add the user data to file
            f.seek(2)
            f.write(email + ':')
            f.write(hash + '\n')
        print("You have registered successfully!")

    else:
        print("Password is not the same!")

    
def login():
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
                print("Logged In Successfully!")
                return
        
        print("Login failed! \n")


while True:
    print("-------------- LOGIN SYSTEM -----------------")
    print("1. Signup")
    print("2. Login")
    print("3. Exit")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        signup()
    elif ch == 2:
        login()
    elif ch == 3:
        break
    else:
        print("Wrong Choice!")