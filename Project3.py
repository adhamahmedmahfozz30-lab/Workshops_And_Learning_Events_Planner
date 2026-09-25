def merge_sort(events,l,h,getter="get_name",order="ascending"):
    if l >= h:
        return
    mid = (l+h)//2
    merge_sort(events,l,mid,getter,order)
    merge_sort(events,mid+1,h,getter,order)
    merge(events,l,mid,h,getter,order)

def merge(events,l,mid,h,getter,order):
    merged = []
    i,j=l,mid+1
    while i<=mid and j<=h:
        val1=getattr(events[i],getter)()
        val2=getattr(events[j],getter)()
        if isinstance(val1,str):
            val1=val1.strip().lower()
            val2=val2.strip().lower()
        if order=="ascending":
            condition= val1<=val2
        else:
            condition = val1>=val2
        if condition:
            merged.append(events[i])
            i += 1
        else:
            merged.append(events[j])
            j += 1
    if i>mid:
        for k in range(j,h+1):
            merged.append(events[k])
    else:
        for k in range(i,mid+1):
            merged.append(events[k])
    for k in range(len(merged)):
        events[l+k] = merged[k]

def binary_search(events, target, getter="get_name"):
    if isinstance(target, str):
        target=target.strip().lower()
    low=0
    high=len(events)-1
    while low<=high:
        mid=(low+high)//2
        mid_value = getattr(events[mid],getter)()
        if isinstance(mid_value, str):
            mid_value=mid_value.strip().lower()
        if mid_value==target:
            return mid
        elif target<mid_value:
            high=mid-1
        else:
            low=mid+1
    return -1


class Event:
    def __init__(self, name, trainer, location, price, duration, rating, avail_seats, category):
        self.set_name(name)
        self.set_trainer(trainer)
        self.set_location(location)
        self.set_price(price)
        self.set_duration(duration)
        self.set_rating(rating)
        self.set_avail_seats(avail_seats)
        self.set_category(category)

    # SETTERS
    def set_name(self, name):
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        self.__name = name

    def set_trainer(self, trainer):
        if not trainer or not trainer.strip():
            raise ValueError("Trainer cannot be empty")
        self.__trainer = trainer

    def set_location(self, location):
        if not location or not location.strip():
            raise ValueError("Location cannot be empty")
        self.__location = location

    def set_price(self, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = price

    def set_duration(self, duration):
        if duration < 0:
            raise ValueError("Duration cannot be negative")
        self.__duration = duration

    def set_avail_seats(self, avail_seats):
        if avail_seats < 0:
            raise ValueError("Available seats cannot be negative")
        self.__avail_seats = avail_seats

    def set_rating(self, rating):
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        self.__rating = rating

    def set_category(self, category):
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")
        self.__category = category

    # GETTERS
    def get_name(self):
        return self.__name

    def get_trainer(self):
        return self.__trainer

    def get_location(self):
        return self.__location

    def get_price(self):
        return self.__price

    def get_duration(self):
        return self.__duration

    def get_rating(self):
        return self.__rating

    def get_avail_seats(self):
        return self.__avail_seats

    def get_category(self):
        return self.__category

    def __str__(self):
        return f"Event(name={self.__name!r}, trainer={self.__trainer!r}, location={self.__location!r}, price={self.__price},duration={self.__duration}, rating={self.__rating}, avail_seats={self.__avail_seats}, category={self.__category!r})"


class LearningPlan:
    def __init__(self, user_governorate):
        self.__user_governorate = user_governorate
        self.__selected_events = []
    def to_list(self):
        """Convert selected events to dictionaries for JSON storage."""
        events_data = []
        for event in self.__selected_events:
            events_data.append({
                "name": event.get_name(),
                "trainer": event.get_trainer(),
                "location": event.get_location(),
                "price": event.get_price(),
                "duration": event.get_duration(),
                "rating": event.get_rating(),
                "avail_seats": event.get_avail_seats(),
                "category": event.get_category()
            })
        return events_data

    def load_list(self, events_data):
        """Restore a saved plan, including an empty list from older accounts."""
        events = []
        for data in events_data:
            events.append(Event(
                data["name"], data["trainer"], data["location"],
                data["price"], data["duration"], data["rating"],
                data["avail_seats"], data["category"]
            ))
        self.__selected_events = events

    def add_event(self, event): #used by student
        self.__selected_events.append(event)
    def remove_event(self, event_name): #used by student
        if not self.__selected_events:
            print("No events selected in Your Plan!")
            return
        merge_sort(self.__selected_events,0,len(self.__selected_events)-1,'get_name')
        searched=binary_search(self.__selected_events,event_name)
        if searched!=-1:
            deleted=self.__selected_events.pop(searched)
            print(f"Removed {deleted.get_name()} from your plan.")
            return
        else:
            print("Event not found in your plan.")
            return
    def calculate_summary(self):
        if not self.__selected_events:
            print("Your plan is empty. Total Cost: 0 EGP")
            return
        total_fees=sum(list(map(lambda event: event.get_price(), self.__selected_events)))
        total_hours=sum(list(map(lambda event: event.get_duration(), self.__selected_events)))
        transp_fees=list(map(lambda event: 30 if event.get_location().strip().lower()==self.__user_governorate.strip().lower() else 100,self.__selected_events))
        total_transp=sum(transp_fees)
        final_cost=total_fees+total_transp
        print(f"Total Learning Hours: {total_hours} hrs")
        print(f"Total Event Fees: {total_fees} EGP")
        print(f"Total Transport Cost: {total_transp} EGP")
        print(f"Final Plan Cost: {final_cost} EGP")
    def view_plan(self):
        if not self.__selected_events:
            print("Your plan is empty!")
            return
        c=1
        print("\n--- My Learning Plan ---")
        for event in self.__selected_events:
            print(f"{c}. {event.get_name()} | Category: {event.get_category()} | Location: {event.get_location()} | Price: {event.get_price()} EGP | Duration: {event.get_duration()} hrs")
            c+=1
        print()


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

