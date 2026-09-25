import json

def load_users():
    with open('users.json', 'r') as file:
        users_data = json.load(file)
        return users_data


def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)


def load_events():
    """Read the event catalogue as a list of dictionaries."""
    with open('events.json', 'r') as file:
        return json.load(file)


def save_events(events):
    """Save the full list of event dictionaries."""
    with open('events.json', 'w') as file:
        json.dump(events, file, indent=4)
