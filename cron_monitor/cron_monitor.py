from flask import Flask, g
from flask_mysqldb import MySQL
from db_client import DB_Client
from log_parser import LogParser
from datetime import datetime,timedelta
import config

app = Flask(__name__)

app.config['MYSQL_USER'] = config.MYSQL_DATABASE_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DATABASE_DB
app.config['MYSQL_HOST'] = config.MYSQL_DATABASE_HOST
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

def connect_db():
  ''' Connect to connection to mysql db'''
  conn = mysql.connection
  return conn

def get_db():
  ''' Get database connection'''
  if not hasattr(g, 'mysql'):
    g.mysql_db = connect_db()
  return g.mysql_db

def init_db():
  ''' Initialise mysql database with schema'''
  mysql_db = get_db()
  with app.open_resource('schema.sql', mode='r') as f:
    db.cursor().executescript(f.read())
  db.commit()
  

@app.route('/')
def log_parser():
  db = get_db()
  end_time = datetime.now()
  start_time = end_time - timedelta(days=1)
  lp = LogParser(start_time, end_time)
  result = lp.parse()
  return str(result)


if __name__ == "__main__":
  app.run()




