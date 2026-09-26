from event_manager import EventManager
from helper_functions import merge_sort
from helper_functions import load_users, save_users, load_events

event_manager = EventManager()
for event in load_events():
    event_manager.add_event(event['name'], event['trainer'], event['location'], event['price'], event['duration'],
                            event['rating'], event['avail_seats'], event['category'])

CATEGORIES = {
    '1': 'Programming',
    '2': 'AI',
    '3': 'Data',
    '4': 'Entrepreneurship',
    '5': 'Design',
    '6': 'Soft Skills'
}


def user_menu(current_user):
    event_manager.events = []
    for event in load_events():
        event_manager.add_event(
            event['name'], event['trainer'], event['location'], event['price'],
            event['duration'], event['rating'], event['avail_seats'], event['category']
        )
    plan = current_user.learning_plan
    print(f'\n--- Welcome, {current_user.name}! ---')

    while True:
        print('\n1) Browse Categories')
        print('2) My Learning Plan')
        print('3) Plan Summary')
        print('4) Logout')
        choice = input('Enter Your Choice: ').strip()

        if choice == '1':
            browse_categories(plan)
        elif choice == '2':
            plan_menu(plan)
        elif choice == '3':
            plan.calculate_summary()
        elif choice == '4':
            users = load_users()
            users[current_user.email]['learning_plan'] = plan.to_list()
            save_users(users)
            return
        else:
            print('Invalid choice! Try again.')


def browse_categories(plan):
    while True:
        print('\n--- Categories ---')
        for number, category in CATEGORIES.items():
            print(f'{number}) {category}')
        print('0) Back')
        choice = input('Enter Your Choice: ').strip()

        if choice == '0':
            return
        elif choice in CATEGORIES:
            category_menu(CATEGORIES[choice], plan)
        else:
            print('Invalid choice! Try again.')


def category_menu(category, plan):
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
                event_details(events[index], plan)
            else:
                print('Invalid event number.')

        elif choice == '2':
            name = input('Event name: ').strip()
            event = Manager.find_event_by_name(name)
            if event is None or event.get_category() != category:
                print('Event not found in this category.')
            else:
                event_details(event, plan)

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
        elif choice == '0':
            return
        else:
            print('Invalid choice! Try again.')



def event_details(event, plan):
    # Both opening and searching use this one details screen.
    # print(f'\n--- {event.get_name()} ---')
    # print(f'Trainer: {event.get_trainer()}')
    # print(f'Location: {event.get_location()}')
    # print(f'Price: {event.get_price()} EGP')
    # print(f'Duration: {event.get_duration()} hours')
    # print(f'Rating: {event.get_rating()}')
    # print(f'Available Seats: {event.get_avail_seats()}')
    # print(f'Category: {event.get_category()}')

    print(event)

    while True:
        print('\n1) Add to My Learning Plan')
        print('0) Back')
        choice = input('Enter Your Choice: ').strip()
        if choice == '1':
            plan.add_event(event)
            return
        elif choice == '0':
            return
        else:
            print('Invalid choice! Try again.')


def plan_menu(plan):
    while True:
        if not plan.view_plan():
            print('\n1) Remove Event')
            print('0) Back')
            choice = input('Enter Your Choice: ').strip()
            if choice == '1':
                name = input('Event name to remove: ').strip()
                plan.remove_event(name)
            elif choice == '0':
                return
            else:
                print('Invalid choice! Try again.')
