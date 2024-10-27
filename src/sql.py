import mysql.connector

LOGGED_IN = False


class sql:

  def __init__(self, host, user, password, database="Minesweeper"):
    global LOGGED_IN

    self.mycon = mysql.connector.connect(host=host, user=user, password=password)

    if not self.mycon.is_connected():
      raise mysql.connector.Error("Failed to connect to MySQL")
    LOGGED_IN = True

    self.table = "Stats"
    self.mycur = self.mycon.cursor()

    self.use_database(database)
    self.create_table()

  def use_database(self, database):
    self.mycur.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    self.mycon.commit()
    self.mycur.execute(f"USE {database}")

  def create_table(self):
    self.mycur.execute(
        f"CREATE TABLE IF NOT EXISTS {self.table} (match_id INT AUTO_INCREMENT, win_or_lose CHAR(1), time INT)"
    )
    self.mycon.commit()
