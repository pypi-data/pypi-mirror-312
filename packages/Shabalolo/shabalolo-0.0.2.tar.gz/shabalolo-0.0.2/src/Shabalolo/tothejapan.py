import json
import os

DATA_FILE = 'user_data.json'

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as file:
        data = json.load(file)
else:
    data = {'uspass': {}, 'codes': {}}

uspass = data['uspass']
codes = data['codes']

class Shabamorg:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        if username in uspass:
            if uspass[username] == password:
                print("You have successfully logged in.\n")
            else:
                print("The password or username is wrong.\n")
        else:
            print("You have successfully registered.\n")
            uspass[username] = password
            self._save_data()

    def get_code(self):
        try:
            return codes[self.username]
        except KeyError:
            print("You don't have a code, use the set_code() method to register your code.\n")

    def set_code(self, code):
        self.code = code
        codes[self.username] = code
        self._save_data()
        print("You have successfully registered your code.\n")

    def _save_data(self):
        data = {'uspass': uspass, 'codes': codes}
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file)