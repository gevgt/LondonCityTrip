import pandas as pd
import os
from location import *
from matplotlib import pyplot as plt, image as mpimg, use
use('Agg')
from sklearn.cluster import KMeans
from collections import OrderedDict
import json

COLORS = {
    0: 'red',
    1: 'blue',
    2: 'orange',
    3: 'green',
    4: 'yellow',
    5: 'purple',
    6: 'pink'
}

COLOR_TO_DAY = {
    'red'   : 0,
    'blue'  : 1,
    'orange': 2,
    'green' : 3,
    'yellow': 4,
    'purple': 5,
    'pink'  : 6
}

class CityTrip:

    def __init__(self):
        self.locations              = []
        self.days                   = None
        self.not_planned_locations  = None
        self.__load_excel()
        self.locations_dict         = dict([(loc.name, loc) for loc in self.locations])

    def assign_location_to_day(self, day_str: str, *args: str):
        if not self.__check_input_day(day_str):
            print('Wrong Input (day)')
            return
        day = COLOR_TO_DAY[day_str]
        for location_name in args:
            if not self.__check_input_locations(location_name):
                print('Wrong Input (location)')
                return
            self.locations_dict[location_name].day_label    = day
            self.locations_dict[location_name].color        = COLORS[day]
        self.__write_planned_days_to_txt()
        self.save_map_with_all_locations()

    def count_locations_for_day(self, day: str):
        print()
        day = COLOR_TO_DAY[day]
        dict_w_location_count = OrderedDict([(loc_type, 0) for loc_type in sorted(list(set(subclass.__name__ for subclass in Location.__subclasses__())))])
        for location in self.days[day]:
            dict_w_location_count[location.__class__.__name__] += 1

        for key in dict_w_location_count:
            print("{: <30} {: <10}".format(f'{key}', f'{dict_w_location_count[key]}'))

        print(f'\nSum: {len(self.days[day])}')

    def is_something_missing(self):
        all_location_types = set([subclass.__name__ for subclass in Location.__subclasses__()])
        for day in self.days:
            available_location_types    = set([location.__class__.__name__ for location in day])
            pubs_and_restaurants        = [location for location in day if location.__class__.__name__ in ['Restaurant', 'Pub']]
            missing_lunch_or_diner      = {'lunch', 'dinner'}.difference([location.lunch_dinner for location in pubs_and_restaurants])
            missing_location_types      = all_location_types.difference(available_location_types).union(missing_lunch_or_diner)
            if missing_location_types:
                print(f'Day {day[0].color.upper()}:')
                [print(mlt) for mlt in missing_location_types]
            print('\n')

    def merge_days(self, day1: str, day2: str):
        if not self.__check_input_day(day1) or not self.__check_input_day(day2):
            print('Wrong input')
            return
        day1        = COLOR_TO_DAY[day1]
        day2        = COLOR_TO_DAY[day2]
        day1, day2  = self.__sort_days(day1, day2)

        for location in self.days[day2]:
            location.day_label = day1
            location.color     = COLORS[day1]
            self.days[day1].append(location)

        self.days[day2] = []
        self.days       = [day for day in self.days if len(day) > 0]

        for i, day in enumerate(self.days):
            for location in day:
                if location.day_label == i:
                    break
                location.day_label = i
                location.color     = COLORS[location.day_label]

        self.__write_planned_days_to_txt()
        self.save_map_with_all_locations()

    def plan_the_days(self, n_days_to_plan):
        locations_df    = pd.DataFrame([(loc.name, loc.coordinates.breitengrad, loc.coordinates.laengengrad) for loc in self.locations], columns=['name', 'breitengrad', 'laengengrad']).set_index('name')
        inputs          = locations_df.values
        kmeans          = KMeans(n_clusters=n_days_to_plan, random_state=0).fit(inputs)

        for location_name, label in zip(locations_df.index, kmeans.labels_):
            self.locations_dict[location_name].day_label    = label
            self.locations_dict[location_name].color        = COLORS[label]

        self.__write_planned_days_to_txt()
        self.save_map_with_all_locations()

    def print_infos_of_location(self, *args: str):
        return  # todo: Fertig machen

    def save_map_with_all_locations(self):
        self.__print_map_with_locations(self.locations, save_map_name='all_locations')

    def save_map_with_certain_day(self, *args):
        for day_number in args:
            self.__print_map_with_locations(self.days[COLOR_TO_DAY[day_number]], save_map_name=f'day_{day_number}')

    def set_part_of_tour(self, location_name: str):
        if location_name not in self.locations_dict.keys():
            print('Wrong input')
            return
        self.locations_dict[location_name].part_of_tour = not self.locations_dict[location_name].part_of_tour
        self.__write_planned_days_to_txt()
        self.save_map_with_all_locations()

    def set_lunch_dining(self, location_name: str, lunch_dinner: str):
        if location_name not in self.locations_dict.keys() or lunch_dinner not in {'lunch', 'dinner'}:
            print('Wrong input')
            return
        self.locations_dict[location_name].lunch_dinner = lunch_dinner
        self.__write_planned_days_to_txt()
        self.save_map_with_all_locations()

    def split_days(self, day: str):
        if not self.__check_input_day(day):
            print('Wrong input')
            return
        day                 = COLOR_TO_DAY[day]
        locations_df        = pd.DataFrame([(loc.name, loc.coordinates.breitengrad, loc.coordinates.laengengrad) for loc in self.days[day]], columns=['name', 'breitengrad', 'laengengrad']).set_index('name')
        inputs              = locations_df.values
        kmeans              = KMeans(n_clusters=2, random_state=0).fit(inputs)
        self.days[day]  = []
        self.days.append([])

        for location_name, label in zip(locations_df.index, kmeans.labels_):
            if label == 1:
                self.locations_dict[location_name].day_label    = len(self.days) - 1
                self.locations_dict[location_name].color         = COLORS[self.locations_dict[location_name].day_label]

        self.__write_planned_days_to_txt()
        self.save_map_with_all_locations()

    def __check_input_day(self, input_day: str):
        available_day_colors = set([day[0].color for day in self.days])
        if input_day in available_day_colors:
            return True
        else:
            return False

    def __check_input_locations(self, input_location: str):
        available_location_names = set([location.name for location in self.locations])
        if input_location in available_location_names:
            return True
        else:
            return False

    def __load_excel(self):
        locations_df = dict([(file[:file.find('.')], pd.read_csv(file, delimiter=';')) for file in os.listdir(os.curdir) if file.endswith('.csv')])

        for _, row in locations_df['pub'].iterrows():
            self.locations.append(
                Pub(
                    name                = row['name'],
                    coordinates         = Coordinates(self.__str_to_float(row['laengengrad']), self.__str_to_float(row['breitengrad'])),
                    price_per_guinnes   = row['price_per_guinnes'],
                    lunch_dinner        = row['lunch_dinner']
                )
            )

        for _, row in locations_df['breakfast'].iterrows():
            self.locations.append(
                Breakfast(
                    name                                = row['name'],
                    coordinates                         = Coordinates(self.__str_to_float(row['laengengrad']), self.__str_to_float(row['breitengrad'])),
                    price_per_full_english_breakfast    = row['price_per_full_english_breakfast'],
                    opening_hour                        = OpeningHour(row['hour'], row['minute'])
                )
            )

        for _, row in locations_df['attractions'].iterrows():
            self.locations.append(
                Attractions(
                    name        = row['name'],
                    coordinates = Coordinates(self.__str_to_float(row['laengengrad']), self.__str_to_float(row['breitengrad'])),
                    price       = row['price']
                )
            )

        for _, row in locations_df['restaurants'].iterrows():
            self.locations.append(
                Restaurant(
                    name            = row['name'],
                    coordinates     = Coordinates(self.__str_to_float(row['laengengrad']), self.__str_to_float(row['breitengrad'])),
                    price_category  = row['price_category'],
                    lunch_dinner    = row['lunch_dinner']
                )
            )

    def __print_map_with_locations(self, locations, save_map_name=None):
        london_map = mpimg.imread('london_map.png')
        f = plt.figure()
        implot = plt.imshow(london_map)

        for location in locations:
            x = (location.coordinates.breitengrad + 0.1941) * (2880 / 0.1944)
            y = abs((location.coordinates.laengengrad - 51.5493) * (1722 / 0.0725))
            color = location.color if location.part_of_tour else 'grey'
            marker_size = 25 if location.part_of_tour else 20
            plt.scatter(x, y, color=color, s=marker_size, marker=location.marker)
            color = 'black' if location.part_of_tour else 'grey'
            fontsize = 3 if location.part_of_tour else 2
            plt.annotate(location.name, (x, y), textcoords="offset points", xytext=(0,4), ha='center', fontsize=fontsize, color=color, weight='bold')
        plt.axis('off')

        if save_map_name:
            f.savefig(f'{save_map_name}.pdf', bbox_inches='tight')

    def __write_planned_days_to_txt(self):
        n_days_to_plan = len(set([location.day_label for location in self.locations]))
        self.days                       = [[] for _ in range(n_days_to_plan)]
        self.not_planned_locations    = []
        for location in self.locations:
            if location.part_of_tour:
                self.days[location.day_label].append(location)
            else:
                self.not_planned_locations.append(location)

        with open('planned_days.txt', 'w') as f:
            for day_n, day in enumerate(self.days + [self.not_planned_locations]):
                line = f'Day {COLORS[day_n].upper()}:'
                if day_n == len(self.days):
                    line = 'Locations that are not included in the planning of the days:'
                print(line)
                f.write(line)
                f.write('\n')
                for location in day:
                    if location.__class__.__name__ in ['Restaurant', 'Pub']:
                        line = "{: <30} {: <20} {: <10}".format(f'{location.name}', f'{location.__class__.__name__}', f'{location.lunch_dinner}')
                    else:
                        line = "{: <30} {: <20}".format(f'{location.name}', f'{location.__class__.__name__}')
                    print(line)
                    f.write(line)
                    f.write('\n')
                line = '\n' * 3
                print(line)
                f.write(line)

    @staticmethod
    def __sort_days(day1, day2):
        days = [day1, day2]
        return min(days), max(days)

    @staticmethod
    def __str_to_float(str):
        return float(str.replace(',', '.'))
