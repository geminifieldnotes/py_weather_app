"""Handle the creation of box and line plots"""
import matplotlib.pyplot as plt
import numpy as np
from db_operations import DBOperations

class PlotOperations:
    """Class for reveiving weather data and ploting"""
    def initialize(self):
      """Initialize the class"""

    def box_plot(self, weather_data):
        """Plots  of mean temperatures in a date range (year to year)"""
        data = []
        for month in weather_data:
            data.append(weather_data[month])

        plt.boxplot(data)
        plt.title(f'Monthly Temperature Distribution for:{start_year} to {end_year}')
        plt.ylabel('Temperature (Celsius)')
        plt.xlabel('Month')
        plt.show()

    def line_plot(self, weather_data):
        """ plot which shows the mean daily temp of a particular month and year"""
        data = []
        dates = []
        for day in weather_data:
            dates.append(day)
            data.append(weather_data[day])

        plt.plot(dates, data)
        plt.title('Daily Avg Temperatures')
        plt.ylabel('Avg Daily Temp')
        plt.xlabel('Day of Month')
        plt.xticks(rotation=45)
        plt.show()

start_year = '2000'
end_year = '2022'
weather_data = DBOperations().fetch_data(start_year, end_year)
PlotOperations().box_plot(weather_data)

year = '2020'
month = '03'
weather_data = DBOperations().fetch_data(year, month)
PlotOperations().line_plot(weather_data)
