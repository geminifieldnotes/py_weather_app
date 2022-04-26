""" This module contains a WeatherProcessor class """
import logging.handlers
from datetime import datetime
from db_operations import DBOperations
from plot_operations import PlotOperations


def export():
    """ Downloads all weather data records into a CSV file """
    try:
        header, rows = DBOperations.fetch_all(DBOperations(), 0)

        f = open('Weather Data.csv', 'w')
        f.write(','.join(header) + '\n')

        for row in rows:
            f.write(','.join(str(r).replace(",", "") for r in row) + '\n')

        f.close()
        logger.info(str(len(rows)) + ' rows written successfully to ' + f.name)
    except Exception as error:
        logger.error("WeatherProcessor:export: %s", error)


def prompt_menu():
    """ Shows menu and prompts for user selection """
    try:
        action = input(
            "Select an action:\n\t[D] - Download a full set of weather data\n\t[U] - Update weather data and "
            "download new records\n\t[B] - Generate a box plot with year range\n\t[L] - Generate a monthly "
            "line plot\n\t[X] - Exit\n\n").strip()
        return action.upper()
    except Exception as error:
        logger.error("WeatherProcessor:prompt_menu: %s", error)


class WeatherProcessor:
    """Presents the user with a menu of choices."""
    logger = logging.getLogger("main." + __name__)

    def __init__(self):
        try:
            user_action = prompt_menu()
            if user_action == 'U':
                logger.info("Updating weather data in progress...")
                DBOperations.update_data(DBOperations())
                logger.info("Updated weather data. Downloading...")
                export()
                logger.info("Download complete")
            elif user_action == 'D':
                logger.info("Downloading full weather data in progress...")
                export()
                logger.info("Download complete")
            elif user_action == 'B':
                from_year = to_year = from_year_input = to_year_input = None
                try:
                    from_year_input = input("Start Year (YYYY):")
                    from_year = datetime.strptime(from_year_input, "%Y").strftime("%Y")
                    to_year_input = input("End Year (YYYY):")
                    to_year = datetime.strptime(to_year_input, "%Y").strftime("%Y")
                except ValueError:
                    if from_year is None:
                        self.restart(from_year_input, 'year')
                    elif to_year is None and from_year is not None:
                        self.restart(to_year_input, 'year')
                weather_data = DBOperations().fetch_data(from_year, to_year)
                PlotOperations().box_plot(weather_data, from_year, to_year)
            elif user_action == 'L':
                year = year_input = month_input = month = None
                try:
                    year_input = input("Year (YYYY):")
                    year = datetime.strptime(year_input, "%Y").strftime("%Y")
                    month_input = input("Month (MM):")
                    month = datetime.strptime(month_input, "%m").strftime("%m")
                except ValueError:
                    if year is None:
                        self.restart(year_input, 'year')
                    elif month is None and year is not None:
                        self.restart(month_input, 'month')
                weather_data = DBOperations().fetch_data(year, month)
                PlotOperations().line_plot(weather_data)
            elif user_action == 'X':
                pass
            else:
                self.restart(user_action, 'action')

            if user_action == 'U' or user_action == 'D' or user_action == 'B' or user_action == 'L':
                restart_action = input(f"Go back to Main Menu?\n\t[Y] - Yes\n\t[Any key] - No\n").upper()
                if restart_action == 'Y':
                    self.__init__()

            logger.info("Application Exited")
            exit()
        except Exception as error:
            logger.error("WeatherProcessor:init: %s", error)

    def restart(self, value, input_type):
        """ Displays the restart menu """
        retry = input(f"{value} is an invalid {input_type}! Restart?\n\t[Y] - Yes\n\t[Any key] - No\n").upper()
        if retry == 'Y':
            self.__init__()
        else:
            return


if __name__ == "__main__":
    logger = None
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
        processor = WeatherProcessor()
        input()
    except Exception as e:
        logger.error("main_thread:main: %s", e)
