""" This module contains a WeatherProcessor class """


class WeatherProcessor:
    def __init__(self, user_action):
        if user_action == 'U':
            print("ACTION:", user_action)
        elif user_action == 'D':
            print("ACTION:", user_action)
        else:
            retry = input(f"{user_action} is an invalid action! Restart?\n\tEnter Y - Yes\n\tEnter any key - No\n")
            if retry == 'Y':
                user_action = input(
                    "Select an action:\n\t[D] - Download a full set of weather data\n\t[U] - Update weather data and "
                    "download new records\n").strip()
                self.__init__(user_action)
            else:
                return


action = input("Select an action:\n\t[D] - Download a full set of weather data\n\t[U] - Update weather data and "
               "download new records\n").strip()
processor = WeatherProcessor(action)