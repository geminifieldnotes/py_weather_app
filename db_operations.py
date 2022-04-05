import sqlite3
from dbcm import DBCM

class DBOperations:

  def initialize_db(self):
    with DBCM("weather.sqlite") as cur:
      try:
        cur.execute("""create table if not exists weatherdata
                        ( id integer primary key autoincrement not null,
                          sample_date text not null,
                          location text not null,
                          max_temp real not null,
                          min_temp real not null,
                          avg_temp real not null);""")
        print("Table created successfully.")
      except Exception as e:
            print("Error creating table:", e)

  def save_date(self,dictionary):
      try:
        sql = """insert into weatherdata (sample_date,location,max_temp,min_temp,avg_temp)
                values (?,?,?,?,?)"""
        try:
          for dates,datas in dictionary.items():
            data = []
            data.append(dates)
            data.append("Winnipeg, MB")
            for key, value in datas.items():
                data.append(value)
            with DBCM("weather.sqlite") as cur:
              cur.execute(sql, data)
          print("Added weatherdata successfully.")
        except Exception as e:
          print("Error: ",e)
      except Exception as e:
        print("Error inserting weatherdata.", e)

  def purge_data(self):
    with DBCM("weather.sqlite") as cur:
      sql= """delete from  weatherdata"""
      for row in cur.execute(sql):
        print(row)
      print(" Purge all the data from the DB. ")

weather_dict = {
            "2018-06-01": {"Max": 12.0, "Min": 5.6, "Mean": 7.1},
            "2018-06-02": {"Max": 22.2, "Min": 11.1, "Mean": 15.5},
            "2018-06-03": {"Max": 31.3, "Min": 29.9, "Mean": 30.0}
        }

db = DBOperations()
db.initialize_db()
db.save_date(weather_dict)
db.purge_data()
