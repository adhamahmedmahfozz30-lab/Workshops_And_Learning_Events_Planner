from event import Event
from helper_functions import merge_sort, binary_search


class EventManager:
    def __init__(self):
        # kept sorted by name , after every update
        self.events = []

    def add_event(self, name, trainer, location, price, duration, rating, avail_seats, category):
    #used by admin
        event = Event(name, trainer, location, price, duration, rating, avail_seats, category)
        self.events.append(event)
        merge_sort(self.events, 0, len(self.events) - 1, "get_name")
        return event

    # allow updating with a flexible set of args
    def update_event(self, name, **args):
        event = self.find_event_by_name(name)
        if event is None:
            return False

        if "name" in args:
            event.set_name(args["name"])
        if "trainer" in args:
            event.set_trainer(args["trainer"])
        if "location" in args:
            event.set_location(args["location"])
        if "price" in args:
            event.set_price(args["price"])
        if "duration" in args:
            event.set_duration(args["duration"])
        if "rating" in args:
            event.set_rating(args["rating"])
        if "avail_seats" in args:
            event.set_avail_seats(args["avail_seats"])
        if "category" in args:
            event.set_category(args["category"])

        # name may have changed, keep the list sorted for binary search
        merge_sort(self.events, 0, len(self.events) - 1, "get_name")
        return True

    def remove_event(self, name): #used by admin
        event = self.find_event_by_name(name)
        if event is None:
            return False
        self.events.remove(event)
        return True

    # Search an event by its name using binary search
    def find_event_by_name(self, name):
        searched = binary_search(self.events, name, "get_name")
        if searched != -1:
            return self.events[searched]
        return None

    def get_all_events(self):
        return self.events

    def get_events_by_category(self, category):
        return [event for event in self.events if event.get_category() == category]

    def get_events_sorted(self, by, order="ascending"):
        # events sorted ascendingly by default
        events_copy = self.events.copy()
        if not events_copy:
            return events_copy
        if by == "price":
            getter= "get_price"
        elif by == "duration":
            getter= "get_duration"
        elif by == "avail_seats":
            getter= "get_avail_seats"
        else:
            raise ValueError("Choose a valid option")
        merge_sort(events_copy, 0, len(events_copy)-1, getter, order)
        return events_copy
