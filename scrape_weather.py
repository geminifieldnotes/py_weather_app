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
        print("START", tag)
        for attr in attrs:
            print("Attribute:", attr)
        if tag == "abbr":
            for attr in attrs:
                if is_date(attr[1]):
                    print("Attribute:", attr)
                    date_holder = parse(attr[1], fuzzy=False).date().strftime('%Y-%m-%d')
                    print("RYAH", date_holder)
        elif tag == "td":
            self.is_element_td = True

    def handle_data(self, data):
        """
        Matches found hex values to corresponding color names
        and stores to colours dictionary
        """
        print("Data:", data)
        # Check if data is a valid Max, Min, or Mean value before inserting to dictionary
        if data == float and self.is_element_td and self.date_holder is not None and self.td_counter < 3:
            self.td_counter = self.td_counter + 1
            self.daily_temps[daily_temp_switch(self.td_counter)] = data
            """
            If Max, Min, and Mean are all collected, then insert daily weather data
            to weather dictionary and restart counter
            """
            if self.td_counter == 3:
                self.weather[self.daily_holder] = self.daily_temps
                print("NEW HOLDER IS")
                print(self.weather)
                self.td_counter = 0
                self.date_holder = None
        self.is_element_td = False


    def fetch_weather_data(self):
        """ Prints out each entry in colours dictionary """
        try:
            context = ssl._create_unverified_context()
            with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174'
                                        '&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5',
                                        context=context) as response:
                html = str(response.read())

            myparser.feed(html)
        except Exception as e:
            print('MyHTMLParser:print_colours', e)


try:
    myparser = WeatherScraper()
    myparser.fetch_weather_data()
except Exception as e:
    print('MyHTMLParser:main', e)
