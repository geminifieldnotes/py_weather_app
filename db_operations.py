"""This model contains a dboperations class with functions to
initialize and create a database, fetch data and purge data."""
import logging
from dbcm import DBCM
from scrape_weather import WeatherScraper


class DBOperations:
    """This class contains functions to
    initialize and save data, fetch data and purge data."""
    logger = logging.getLogger("main." + __name__)

    def initialize_db(self):
        """creates the table."""
        with DBCM("weather.sqlite") as cur:
            try:
                cur.execute("""create table if not exists weatherdata
                                ( id integer primary key autoincrement not null,
                                  sample_date text unique,
                                  location text not null,
                                  max_temp real not null,
                                  min_temp real not null,
                                  avg_temp real not null);""")
                print("Table created successfully.")
            except Exception as error:
                self.logger.error("Error creating table: %s", error)

    def save_date(self, dictionary):
        """insert all the data from the DB"""
        try:
            sql = """insert into weatherdata (sample_date,location,max_temp,min_temp,avg_temp)
                    values (?,?,?,?,?)"""
            try:
                with DBCM("weather.sqlite") as cur:
                    for date, temp in dictionary.items():
                        data = []
                        data.append(date)
                        data.append("Winnipeg, MB")
                        for value in temp.items():
                            record = iter(value)
                            temp_dict = dict(zip(record, record))
                            for key in temp_dict:
                                record = temp_dict.get(key)
                                data.append(record)
                        cur.execute(sql, data)
                    print("Added weatherdata successfully.")
            except Exception as error:
                self.logger.error("Error: %s", error)
        except Exception as error:
            self.logger.error("Error inserting weatherdata: %s", error)

    def fetch_data(self, arg1, arg2):
        """fetch some data from the DB"""
        if len(arg2) == 4:
            sql = """select sample_date,avg_temp from weatherdata
                      where sample_date>={} and sample_date< {}""".format(arg1, arg2)
            box_plot_dictionary = {}
            try:
                with DBCM("weather.sqlite") as cur:
                    for row in cur.execute(sql):
                        month = int(row[0][5:7])
                        if month not in box_plot_dictionary:
                            box_plot_dictionary[month] = [row[1]]
                        else:
                            box_plot_dictionary[month].append(row[1])
            except Exception as error:
                self.logger.error("Organizing line box data for box plot: %s", error)
            return box_plot_dictionary
        else:
            sql = """select sample_date,avg_temp from weatherdata where strftime
                      ('%Y-%m', sample_date)='{}-{}'""".format(arg1, arg2)
            line_plot_dictionary = {}
            try:
                with DBCM("weather.sqlite") as cur:
                    for row in cur.execute(sql):
                        line_plot_dictionary[row[0]] = row[1]
            except Exception as error:
                self.logger.error("Organizing line box data for line plot: %s", error)
            return line_plot_dictionary

    def purge_data(self):
        """Deletes all the data from the DB"""
        try:
            with DBCM("weather.sqlite") as cur:
                sql = """delete from  weatherdata"""
                for row in cur.execute(sql):
                    print(row)
        except Exception as error:
            self.logger.error("Delete all the data from the DB: %s", error)

    def is_empty(self):
        """ Checks if Weather table is populated """
        sql = """SELECT CASE WHEN EXISTS(SELECT 1 FROM weatherdata) THEN 0 ELSE 1 END"""
        try:
            with DBCM("weather.sqlite") as cur:
                for row in cur.execute(sql):
                    return row[0]
        except Exception as error:
            self.logger.error("Organizing line box data for line plot: %s", error)

try:
    weather = WeatherScraper()
    db = DBOperations()

    if db.is_empty() == 1:
        weather.fetch_weather_data()
        print("Finished scraping all available weather records")
        db.initialize_db()
        db.purge_data()
        db.save_date(weather.weather)
except Exception as e:
    print('DBOperations:main', e)
