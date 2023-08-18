import os
from cryptography.fernet import Fernet
from bcrypt import gensalt, hashpw
import json


def load_key():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key


def write_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)


if os.path.isfile("data.json") and os.path.getsize("data.json") > 0:
    with open("data.json", "r+") as data:
        json_data = json.load(data)
        master_pwd = input("Enter Master Password: ")

        if json_data["masterPassword"] == str(hashpw(bytes(master_pwd, 'utf-8'), gensalt(14))):
            print("Passwords do not match")
            exit(101)

        key = load_key() + master_pwd.encode()
        fer = Fernet(key)

        if not json_data["keyCreated"]: write_key()
else:
    write_key()
    mas_pwd = input("Enter a new Master Password: ")
    password = str(hashpw(bytes(mas_pwd, 'utf-8'), gensalt(14)))

    json_data = {
        "firstTime": True,
        "keyCreated": True,
        "masterPassword": password,
    }

    with open('data.json', 'w') as json_file:
        json.dump(json_data, json_file)


def view():
    print("View Mode")

    if os.path.isfile("passwords.txt") and os.path.getsize("passwords.txt") > 0:
        with open('passwords.txt', 'r+') as f:
            f.seek(0)

            for line in f.readlines():
                data = line.rstrip()
                user, pwd = data.split("|")

                print("-----------------------")
                print("User Name: " + user + "\nPassword: " + fer.decrypt(pwd.encode()).decode())
                print("-----------------------")
                print("\n")
    else:
        print("No Accounts stored")


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
