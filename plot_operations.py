"""Handle the creation of box and line plots"""
import logging
import matplotlib.pyplot as plt
from db_operations import DBOperations

class PlotOperations:
    """Class for reveiving weather data and ploting"""
    def initialize(self):
        """Initialize the class"""

    def box_plot(self, weather_datas, from_year, to_year):
        """Plots  of mean temperatures in a date range (year to year)"""
        data = []
        try:
            for month in weather_datas:
                data.append(weather_datas[month])
        except Exception as error:
            logging.warning("Error: Organizing line box data: %s",error)

        try:
            plt.boxplot(data)
            plt.title(f'Monthly Temperature Distribution for:{from_year} to {to_year}')
            plt.ylabel('Temperature (Celsius)')
            plt.xlabel('Month')
            plt.show()
        except Exception as error:
            logging.warning("Error: Create box plot: %s",error)


    def line_plot(self, weather_datas):
        """ plot which shows the mean daily temp of a particular month and year"""
        data = []
        dates = []
        try:
            for day in weather_datas:
                dates.append(day)
                data.append(weather_datas[day])
        except Exception as error:
            logging.warning("Error: Organizing line plot data: %s",error)
        try:
            plt.plot(dates, data)
            plt.title('Daily Avg Temperatures')
            plt.ylabel('Avg Daily Temp')
            plt.xlabel('Day of Month')
            plt.xticks(rotation=45)
            plt.show()
        except Exception as error:
            logging.warning("Error: Create line plot: %s",error)
