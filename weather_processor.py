""" This module contains a WeatherProcessor class """

from db_operations import DBOperations
from plot_operations import PlotOperations


class WeatherProcessor:
    def __init__(self, user_action):
        try:
            if user_action == 'U':
                print("Updating weather data in progress...")
            elif user_action == 'D':
                print("Downloading full weather data in progress...")
            elif user_action == 'B':
                from_year = input("Start Year:")
                to_year = input("End Year:")
                weather_data = DBOperations().fetch_data(from_year, to_year)
                PlotOperations().box_plot(weather_data, from_year, to_year)
            elif user_action == 'L':
                month = input("Month:")
                year = input("Year:")
                weather_data = DBOperations().fetch_data(year, month)
                PlotOperations().line_plot(weather_data)
            elif user_action == 'X':
                return
            else:
                retry = input(f"{user_action} is an invalid action! Restart?\n\t[Y] - Yes\n\t[Any key] - No\n")
                if retry == 'Y':
                    user_action = input(
                        "Select an action:\n\t[D] - Download a full set of weather data\n\t[U] - Update weather data and "
                        "download new records\n\t[B] - Generate a box plot with year range\n\t[L] - Generate a monthly "
                        "line plot\n\t[X] - Exit\n\n").strip()
                    self.__init__(user_action)
                else:
                    return
        except Exception as e:
            print('WeatherProcessor:init', e)


try:
    action = input("Select an action:\n\t[D] - Download a full set of weather data\n\t[U] - Update weather data and "
                   "download new records\n\t[B] - Generate a box plot with year range\n\t[L] - Generate a monthly line "
                   "plot\n\t[X] - Exit\n\n").strip()
    processor = WeatherProcessor(action)
    input()
except Exception as e:
    print('WeatherProcessor:main', e)
