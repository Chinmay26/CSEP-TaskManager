from flask import g

class DB_Client:
  '''
     Simple MySQL DB client interface to execute queries with mysql database
  '''
  def __init__(self):
    self.mysql = g.mysql_db


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
    if hasattr(g, 'mysql'):
      g.mysql.close()

  def execute_sql_command(self, sql_command, arg_list=None):
    c = self.mysql.cursor()
    c.execute(sql_command, arg_list)
    self.mysql.commit()
    results = c.fetchall()
    return results



