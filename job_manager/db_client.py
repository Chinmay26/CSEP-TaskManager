import sqlite3 as db

class DB_Client:
  '''
     Simple SQLite3 DB client interface to execute queries with sqlite3 database
  '''
  def __init__(self, db_file_path):
    self.db_connection = db.connect(db_file_path)

  def save_to_db(sef):
    try:
      self.db_connection.commit()
    except db.Error as e:
      if self.db_connection:
        self.db_connection.rollback()
      #To-Do Handle Error
      print("Error while saving to db: %s" % e.args[0])
    finally:
      self.close_connection()

  def close_connection(self):
    if self.db_connection:
      self.db_connection.close()

  def execute_sql_command(self, sql_command):
    self.db_connection.row_factory = db.Row
    c = self.db_connection.cursor()
    results = c.execute(sql_command)
    return results
