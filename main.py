from os.path import getsize
from cryptography.fernet import Fernet


def load_key():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key


master_pwd = input("Enter Master Password: ")
key = load_key() + master_pwd.encode()
fer = Fernet(key)

'''def write_key():
    key = Fernet.generate_key()

    with open('key.key', 'wb') as key_file:
        key_file.write(key)'''


def view():
    print("View Mode")

    if getsize('passwords.txt') == 0:
        print("No Accounts stored")
        return

    with open('passwords.txt', 'r+') as f:
        f.seek()
        for line in f.readlines():
            data = line.rstrip()
            user, pwd = data.split("|")

            print("-----------------------")
            print("User Name: " + user + "\nPassword: " + fer.decrypt(pwd.encode()).decode())
            print("-----------------------")
            print("\n")


def add():
    print("Add Mode")

    name = input("Account Name: ")
    pwd = input("Password: ")

    with open('passwords.txt', 'a+') as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")
        print("Saved...")


while True:
    print("1. Add a new password")
    print("2. View Saved passwords")
    print("3. Quit")
    mode = input("Your choice: ")

    if mode == "3":
        break

    if mode == "1":
        add()
    elif mode == "2":
        view()
    else:
        print("Enter a valid choice")
        continue
