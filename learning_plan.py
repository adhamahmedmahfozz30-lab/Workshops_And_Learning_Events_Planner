from event import Event
from helper_functions import merge_sort, binary_search


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
            return None
        c=1
        print("\n--- My Learning Plan ---")
        for event in self.__selected_events:
            print(f"{c}. {event.get_name()} | Category: {event.get_category()} | Location: {event.get_location()} | Price: {event.get_price()} EGP | Duration: {event.get_duration()} hrs")
            c+=1
        print()
