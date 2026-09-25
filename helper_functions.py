import json

def load_users():
    with open('users.json', 'r') as file:
        users_data = json.load(file)
        return users_data


def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)