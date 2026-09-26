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
