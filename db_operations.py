"""This model contains a dboperations class with functions to
initialize and create a database, fetch data and purge data."""
import sqlite3
from dbcm import DBCM
from test import WeatherScraper

class DBOperations:
  """This class contains functions to
  initialize and save data, fetch data and purge data."""
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
      except Exception as e:
            print("Error creating table:", e)

  def save_date(self,dictionary):
    """insert all the data from the DB"""
    try:
      sql = """insert into weatherdata (sample_date,location,max_temp,min_temp,avg_temp)
              values (?,?,?,?,?)"""
      try:
        with DBCM("weather.sqlite") as cur:
          for dates,datas in dictionary.items():
            data = []
            data.append(dates)
            data.append("Winnipeg, MB")
            for key, value in datas.items():
                data.append(value)
            cur.execute(sql, data)
          print("Added weatherdata successfully.")
      except Exception as e:
        print("Error: ",e)
    except Exception as e:
      print("Error inserting weatherdata.", e)

  def fetch_data(self, arg1, arg2):
    """fetch some data from the DB"""
    if len(arg2)==4:
        sql = """select sample_date,avg_temp from weatherdata where sample_date>={} and sample_date< {}""".format(arg1,arg2)
        box_plot_dictionary = {}
        with DBCM("weather.sqlite") as cur:
            for row in cur.execute(sql):
                month = int(row[0][5:7])
                if month not in box_plot_dictionary:
                    box_plot_dictionary[month] = [row[1]]
                else:
                    box_plot_dictionary[month].append(row[1])
        return box_plot_dictionary
    else:
        sql = """select sample_date,avg_temp from weatherdata where strftime('%Y-%m', sample_date)='{}-{}'""".format(arg1,arg2)
        line_plot_dictionary = {}
        with DBCM("weather.sqlite") as cur:
            for row in cur.execute(sql):
                line_plot_dictionary[row[0]] = row[1]
        return line_plot_dictionary

  def purge_data(self):
    """purge all the data from the DB"""
    with DBCM("weather.sqlite") as cur:
      sql= """delete from  weatherdata"""
      for row in cur.execute(sql):
        print(row)
      print(" Purge all the data from the DB. ")

