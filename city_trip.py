import pandas as pd
import os
from location import *
from matplotlib import pyplot as plt, image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

class CityTrip:

    def __init__(self):
        self.locations = []

    @staticmethod
    def str_to_float(str):
        return float(str.replace(',', '.'))

    def load_excel(self):
        locations_df = dict([(file[:file.find('.')], pd.read_csv(file, delimiter=';')) for file in os.listdir(os.curdir) if file.endswith('.csv')])

        for _, row in locations_df['pub'].iterrows():
            self.locations.append(
                Pub(
                    name = row['name'],
                    coordinates = Coordinates(self.str_to_float(row['laengengrad']), self.str_to_float(row['breitengrad'])),
                    dining = True if row['dining'] == 1 else False,
                    price_per_guinnes = row['price_per_guinnes']
                )
            )

        for _, row in locations_df['breakfast'].iterrows():
            self.locations.append(
                Breakfast(
                    name = row['name'],
                    coordinates =  Coordinates(self.str_to_float(row['laengengrad']), self.str_to_float(row['breitengrad'])),
                    price_per_full_english_breakfast = row['price_per_full_english_breakfast'],
                    opening_hour = OpeningHour(row['hour'], row['minute'])
                )
            )


    def print_map_with_locations(self):
        london_map = mpimg.imread('london_map.png')

        f = plt.figure()

        implot = plt.imshow(london_map)

        for location in self.locations:
            x = (location.coordinates.breitengrad + 0.1941) * (2880 / 0.1944)
            y = abs((location.coordinates.laengengrad - 51.5493) * (1722 / 0.0725))
            plt.scatter(x, y, color=location.color, s=40)
            plt.annotate(location.name, (x, y), textcoords="offset points", xytext=(0,4), ha='center', fontsize=3, color="black", weight='bold')
        plt.show()
        f.savefig('map.pdf')