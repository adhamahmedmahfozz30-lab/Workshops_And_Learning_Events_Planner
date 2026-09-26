import math
from event_manager import EventManager
from helper_functions import merge_sort
from helper_functions import load_events, save_events

event_manager = EventManager()

CATEGORIES = {
    '1': 'Programming',
    '2': 'AI',
    '3': 'Data',
    '4': 'Entrepreneurship',
    '5': 'Design',
    '6': 'Soft Skills'
}


def admin_menu(current_user):
    for event in load_events():
        event_manager.add_event(
            event['name'], event['trainer'], event['location'], event['price'],
            event['duration'], event['rating'], event['avail_seats'], event['category']
        )

    print(f'\n--- Admin Dashboard: {current_user.name} ---')
    print('Choose a category to manage its events. Choose Back to log out.')
    browse_categories()


def browse_categories():
    while True:
        print('\n--- Categories ---')
        for number, category in CATEGORIES.items():
            print(f'{number}) {category}')
        print('0) Back')
        choice = input('Enter Your Choice: ').strip()

        if choice == '0':
            return
        elif choice in CATEGORIES:
            category_menu(CATEGORIES[choice])
        else:
            print('Invalid choice! Try again.')


def category_menu(category):
    Manager = event_manager
    events = Manager.get_events_by_category(category)

    while True:
        print(f'\n--- {category} ---')
        if not events:
            print('No events in this category yet.')
        number = 1
        for event in events:
            print(f'{number}) {event.get_name()} | {event.get_price()} EGP | {event.get_duration()} hours')
            number += 1

        print('\n1) Open Event')
        print('2) Search by Name')
        print('3) Sort Events')
        print('4) Default Order')
        print('5) Add Event')
        print('0) Back')
        choice = input('Enter Your Choice: ').strip()

        if choice == '1':
            selected = input('Event number (0 to cancel): ').strip()
            if selected == '0':
                continue
            try:
                index = int(selected) - 1  # check if it is an int
            except ValueError:
                print('Invalid event number.')
                continue
            if 0 <= index < len(events):
                admin_event_details(events[index])
                events = Manager.get_events_by_category(category)
            else:
                print('Invalid event number.')

        elif choice == '2':
            name = input('Event name: ').strip()
            event = Manager.find_event_by_name(name)
            if event is None or event.get_category() != category:
                print('Event not found in this category.')
            else:
                admin_event_details(event)
                events = Manager.get_events_by_category(category)

        elif choice == '3':
            print('1) By Price')
            print('2) By Duration')
            field = input().strip()
            if field == '1':
                getter = "get_price"
            elif field == '2':
                getter = "get_duration"
            else:
                print('Invalid sorting choice.')
                continue

            print('1) Ascending')
            print('2) Descending')
            direction = input('Order: ').strip()
            if direction == '1':
                order = 'ascending'
            elif direction == '2':
                order = 'descending'
            else:
                print('Invalid sorting choice.')
                continue
            merge_sort(events, 0, len(events) - 1, getter, order)

        elif choice == '4':
            events = Manager.get_events_by_category(category)
        elif choice == '5':
            add_event(category)
            events = Manager.get_events_by_category(category)
        elif choice == '0':
            return
        else:
            print('Invalid choice! Try again.')




def save_catalogue(manager):
    events = []
    for event in manager.get_all_events():
        events.append({
            'name': event.get_name(),
            'trainer': event.get_trainer(),
            'location': event.get_location(),
            'price': event.get_price(),
            'duration': event.get_duration(),
            'rating': event.get_rating(),
            'avail_seats': event.get_avail_seats(),
            'category': event.get_category()
        })
    save_events(events)


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print('This field cannot be empty.')


def read_number(prompt, whole=False, maximum=None):
    while True:
        try:
            if whole:
                value = int(input(prompt).strip())
            else:
                value = float(input(prompt).strip())
            if not math.isfinite(value) or value < 0:
                print('Enter a non-negative number.')
                continue
            if maximum is not None and value > maximum:
                print(f'Enter a number between 0 and {maximum}.')
                continue
            return value
        except ValueError:
            print('Invalid number! Try again.')


def read_event_name(manager, current_event=None):
    while True:
        name = read_text('Event Name: ')
        existing = manager.find_event_by_name(name)
        if existing is None or existing is current_event:
            return name
        print('An event with this name already exists.')


def add_event(category):
    manager = event_manager
    print(f'\n--- Add Event to {category} ---')
    name = read_event_name(manager)
    trainer = read_text('Trainer: ')
    location = read_text('Location / Governorate: ')
    price = read_number('Price: ')
    duration = read_number('Duration in hours: ')
    rating = read_number('Rating (0-5): ', maximum=5)
    seats = read_number('Available Seats: ', whole=True)
    manager.add_event(name, trainer, location, price, duration, rating, seats, category)
    save_catalogue(manager)
    print('Event added and saved.')


def admin_event_details(event):
    manager = event_manager
    while True:
        print(event)
        print('\n1) Update Event')
        print('2) Remove Event')
        print('0) Back to Category')
        choice = input('Enter Your Choice: ').strip()
        if choice == '1':
            update_event(event)
        elif choice == '2':
            confirm = input('Remove this event? (y/n): ').strip().lower()
            if confirm == 'y':
                manager.remove_event(event.get_name())
                save_catalogue(manager)
                print('Event removed and saved.')
                return
        elif choice == '0':
            return
        else:
            print('Invalid choice! Try again.')


def update_event(event):
    manager = event_manager
    print('\n--- Update Event ---')
    print('1) Name')
    print('2) Trainer')
    print('3) Location')
    print('4) Price')
    print('5) Duration')
    print('6) Rating')
    print('7) Available Seats')
    print('8) Category')
    print('0) Back')
    choice = input('Enter Your Choice: ').strip()
    changes = {}
    if choice == '1':
        name = read_event_name(manager, event)
        # The existing update_event(name, **args) cannot accept a new name.
        # Reuse the Event setter and their sort without changing their class.
        event.set_name(name)
        merge_sort(manager.events, 0, len(manager.events) - 1, 'get_name')
    elif choice == '2':
        changes['trainer'] = read_text('Trainer: ')
    elif choice == '3':
        changes['location'] = read_text('Location / Governorate: ')
    elif choice == '4':
        changes['price'] = read_number('Price: ')
    elif choice == '5':
        changes['duration'] = read_number('Duration in hours: ')
    elif choice == '6':
        changes['rating'] = read_number('Rating (0-5): ', maximum=5)
    elif choice == '7':
        changes['avail_seats'] = read_number('Available Seats: ', whole=True)
    elif choice == '8':
        for number, category in CATEGORIES.items():
            print(f'{number}) {category}')
        selected = input('Choose Category: ').strip()
        if selected not in CATEGORIES:
            print('Invalid category.')
            return
        changes['category'] = CATEGORIES[selected]
    elif choice == '0':
        return
    else:
        print('Invalid choice! Try again.')
        return

    if changes:
        manager.update_event(event.get_name(), **changes)
    save_catalogue(manager)
    print('Event updated and saved.')
