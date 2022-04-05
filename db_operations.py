import sqlite3

class DBOperations:
  def __init__(self, db_file):
    try:
        self.conn = sqlite3.connect("weather.sqlite")
        print("Opened database successfully.")
    except Exception as e:
            print("Error opening DB:", e)


  def initialize_db(self):
    try:
      self.c = self.conn.cursor()
      self.c.execute("""create table IF NOT EXISTS weatherdata
                        (id integer primary key autoincrement not null,
                        sample_date text not null,
                        location text not null,
                        min_temp real not null,
                        max_temp real not null,
                        avg_temp real not null);""")
      self.conn.commit()
      print("Table created successfully.")
    except Exception as e:
      print("Error creating table:", e)

  def fetch_data(self,dictionary):

    sql = """insert into samples (date,location,max_temp,min_temp,avg_temp)
                  values (?,?,?,?,?)"""

    for dates,datas in dictionary.items():
      self.data = []
      self.data.append(dates)
      self.data.append("Winnipeg")
      for key, value in datas.items():
        self.data.append(value)
        self.c.execute(sql, self.data)
        self.conn.commit()
      print("Added sample successfully.")

  def save_data(self):
    try:
      for row in self.c.execute("select * from weatherdata"):
          print(row)
    except Exception as e:
        print("Error fetching samples.", e)
    self.conn.close()
