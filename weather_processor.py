""" This module contains a WeatherProcessor class """
import logging.handlers
from db_operations import DBOperations
from plot_operations import PlotOperations


class WeatherProcessor:
    """Presents the user with a menu of choices."""
    logger = logging.getLogger("main." + __name__)

    def __init__(self):
        try:
            user_action = self.prompt_menu()
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
                year = input("Year:")
                month = input("Month:")
                weather_data = DBOperations().fetch_data(year, month)
                PlotOperations().line_plot(weather_data)
            elif user_action == 'X':
                return
            else:
                retry = input(f"{user_action} is an invalid action! Restart?\n\t[Y] - Yes\n\t[Any key] - No\n")
                if retry == 'Y':
                    self.__init__()
                else:
                    print("Application Exited")
                    return

            restart_action = input(f"Go back to Main Menu?\n\t[Y] - Yes\n\t[Any key] - No\n")
            if restart_action == 'Y':
                self.__init__()
            else:
                print("Application Exited")
                return
        except Exception as error:
            self.logger.error("WeatherProcessor:init: %s", error)

    def prompt_menu(self):
        """ Shows menu and prompts for user selection """
        try:
            action = input(
                "Select an action:\n\t[D] - Download a full set of weather data\n\t[U] - Update weather data and "
                "download new records\n\t[B] - Generate a box plot with year range\n\t[L] - Generate a monthly "
                "line plot\n\t[X] - Exit\n\n").strip()
            return action
        except Exception as error:
            self.logger.error("WeatherProcessor:prompt_menu: %s", error)


try:
    processor = WeatherProcessor()
    input()
except Exception as e:
    print('WeatherProcessor:main', e)

if __name__ == "__main__":
    try:
        logger = logging.getLogger("main")
        logger.setLevel(logging.DEBUG)
        fh = logging.handlers.RotatingFileHandler(filename="threads.log",
                                                  maxBytes=10485760,
                                                  backupCount=10)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.info("Main Thread Started")
        WeatherProcessor().main()
    except Exception as e:
        logger.error("main_thread:main: %s", e)
