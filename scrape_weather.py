""" This module contains a WeatherScraper HTML parser class """

from html.parser import HTMLParser
import urllib.request
from dateutil.parser import parse

import ssl


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
    date_holder = None

    td_counter = 0
    is_element_td = False

    def handle_starttag(self, tag, attrs):
        """ Checks if an element contains daily weather data """
        try:
            if tag == "abbr":
                for attr in attrs:
                    if is_date(attr[1]):
                        self.date_holder = parse(attr[1], fuzzy=False).date().strftime('%Y-%m-%d')
            elif tag == "td":
                self.is_element_td = True
        except Exception as e:
            print('WeatherScraper:handle_starttag:', e)

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
                        self.weather.update({self.date_holder: self.daily_temps})
                        print(self.weather)
                        self.td_counter = 0
                        self.date_holder = None
                        self.daily_temps = {}

                    self.is_element_td = False
        except Exception as e:
            print('WeatherScraper:handle_data:', e)

    def fetch_weather_data(self):
        """ Records the daily temperatures based on the given date """
        try:
            context = ssl._create_unverified_context()
            with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174'
                                        '&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5',
                                        context=context) as response:
                html = str(response.read())

            self.feed(html)
        except Exception as e:
            print('WeatherScraper:fetch_weather_data', e)


try:
    weather_parser = WeatherScraper()
    weather_parser.fetch_weather_data()
except Exception as e:
    print('WeatherScraper:main', e)
