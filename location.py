from help_classes import *


class Location:

    def __init__(self, name: str, coordinates: Coordinates):
        self.name           = name
        self.coordinates    = coordinates
        self.day_label      = None
        self.part_of_tour   = True
        self.color          = 'grey'


class Pub(Location):

    def __init__(self, name: str, coordinates: Coordinates, dining: bool, price_per_guinnes: float):
        super().__init__(name, coordinates)
        self.dining             = dining
        self.price_per_guinnes  = price_per_guinnes
        self.marker             = '*'


class Breakfast(Location):

    def __init__(self, name: str, coordinates: Coordinates, price_per_full_english_breakfast: float, opening_hour: OpeningHour):
        super().__init__(name, coordinates)
        self.price_per_full_english_breakfast   = price_per_full_english_breakfast
        self.opening_hour                       = opening_hour
        self.marker                             = 'D'


class Restaurant(Location):

    def __init__(self, name: str, coordinates: Coordinates, price_category: int, lunch_dinner: str):
        super().__init__(name, coordinates)
        self.price_category = price_category
        self.lunch_dinner   = lunch_dinner
        self.marker         = 's'


class Attractions(Location):

    def __init__(self, name: str, coordinates: Coordinates, price: float):
        super().__init__(name, coordinates)
        self.price  = price
        self.marker = 'o'