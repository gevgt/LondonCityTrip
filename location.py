from help_classes import *


class Location:

    def __init__(self, name: str, coordinates: Coordinates, day_label: int, part_of_tour: bool):
        self.name           = name
        self.coordinates    = coordinates
        self.day_label      = day_label
        self.part_of_tour   = True


class Pub(Location):

    def __init__(self, name: str, coordinates: Coordinates, day_label: int, part_of_tour: bool, dining: bool, price_per_guinnes: float):
        super().__init__(name, coordinates, day_label, part_of_tour)
        self.dining             = dining
        self.price_per_guinnes  = price_per_guinnes


class Breakfast(Location):

    def __init__(self, name: str, coordinates: Coordinates, day_label: int, part_of_tour: bool, price_per_full_english_breakfast: float, opening_hour: OpeningHour):
        super().__init__(name, coordinates, day_label, part_of_tour)
        self.price_per_full_english_breakfast   = price_per_full_english_breakfast
        self.opening_hour                       = opening_hour


class Restaurant(Location):

    def __init__(self, name: str, coordinates: Coordinates, day_label: int, part_of_tour: bool, price_category: int, lunch_dinner: str):
        super().__init__(name, coordinates, day_label, part_of_tour)
        self.price_category = price_category
        self.lunch_dinner   = lunch_dinner