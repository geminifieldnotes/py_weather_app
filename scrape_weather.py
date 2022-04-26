"""
This module contains a WeatherScraper HTML parser class
Authors: Mariah Garcia, Xueting Hao
"""
import logging
from html.parser import HTMLParser
import urllib.request
from datetime import date
import ssl
from dateutil.parser import parse


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def daily_temp_switch(position):
    """ Returns the appropriate key based on temperature value index """
    switch = {
        1: "Max",
        2: "Min",
        3: "Mean"
    }
    return switch.get(position, None)


class WeatherScraper(HTMLParser):
    """ Contains functions to scrape Winnipeg weather data from the Environment Canada website """
    weather = {}
    daily_temps = {}
    date_holder = None  # holds each day of month upon recording
    given_date = None  # holds each month transition date

    td_counter = 0
    is_element_td = False
    eom_matcher = None
    has_available_record = False

    logger = logging.getLogger("main." + __name__)

    def handle_starttag(self, tag, attrs):
        """ Checks if an element contains daily weather data """
        try:
            if tag == "meta":
                for attr in attrs:
                    if self.given_date.strftime('%B') in attr[1] \
                            and self.given_date.strftime("%Y") in attr[1]:
                        self.has_available_record = True
            if tag == "abbr":
                for attr in attrs:
                    if is_date(attr[1]):
                        self.date_holder = parse(attr[1], fuzzy=False).date()
            elif tag == "td":
                self.is_element_td = True
        except Exception as error:
            self.logger.error("WeatherScraper:handle_starttag: %s", error)

    def handle_data(self, data):
        """
        Matches found temperature values to a new daily weather dictionary
        and stores each daily entry to the weather dictionary
        """
        try:
            if data == 'M':
                is_valid_temp = True
                data = 0.0
            else:
                is_valid_temp = '.' in data and data.replace('.', '', 1).lstrip('E').lstrip('-').isdigit()

            if is_valid_temp:
                # Check if data is a valid Max, Min, or Mean value before inserting to dictionary
                if self.is_element_td and self.date_holder is not None and self.td_counter < 3:
                    self.td_counter = self.td_counter + 1
                    self.daily_temps[daily_temp_switch(self.td_counter)] = float(data)

                    """
                    If Max, Min, and Mean are all collected, then insert daily weather data
                    to weather dictionary and restart counter
                    """
                    if self.td_counter == 3:
                        self.weather.update({self.date_holder.strftime('%Y-%m-%d'): self.daily_temps})
                        # date placeholder for checking if date is end of month
                        self.eom_matcher = self.date_holder

                        # Reset local variables
                        self.td_counter = 0
                        self.date_holder = None
                        self.daily_temps = {}
                        self.is_element_td = False
                        self.has_available_record = False

                        if self.eom_matcher.month == 1:
                            prev_date = self.eom_matcher.replace(self.eom_matcher.year - 1, 12, 1)
                        else:
                            prev_date = self.eom_matcher.replace(self.eom_matcher.year,
                                                                 self.eom_matcher.month - 1, 1)
                        self.given_date = prev_date
        except Exception as error:
            self.logger.error("WeatherScraper:handle_data: %s", error)

    def fetch_weather_data(self, report_date=date.today(), oldest_db_date=None):
        """ Records the daily temperatures based on the given date """
        try:
            self.given_date = report_date
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(
                    f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID"
                    f"=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Ye"
                    f"ar={report_date.year}&Month={report_date.month}",
                    context=context) as response:

                html = str(response.read())

            self.feed(html)

            if oldest_db_date and oldest_db_date == report_date:
                return
            if report_date == self.given_date and self.has_available_record is False:
                return
            elif report_date == self.given_date and self.has_available_record is True:
                # Still get previous month if monthly record is just missing but available
                print(f"Processing {report_date.year} {report_date.month}")
                if self.given_date.month == 1:
                    self.given_date = self.given_date.replace(self.given_date.year - 1, 12, 1)
                else:
                    self.given_date = self.given_date.replace(self.given_date.year,
                                                              self.given_date.month - 1, 1)
                self.fetch_weather_data(self.given_date, oldest_db_date)
            else:
                print(f"Processing {report_date.year} {report_date.month}")
                self.fetch_weather_data(self.given_date, oldest_db_date)
        except RuntimeError as error:
            self.logger.error("WeatherScraper:fetch_weather_data: %s", error)
