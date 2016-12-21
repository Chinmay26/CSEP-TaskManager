from flask import Flask, g
from flask_mysqldb import MySQL
from db_client import DB_Client
from log_parser import LogParser
from datetime import datetime,timedelta
import config
import csv

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
  c = mysql_db.cursor()
  #Setup metadata of jobs
  with open('./data/csep_job_metadata.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    job_id = 1
    for row in csv_reader:

      c.execute('''INSERT INTO jobs(id, job_name, script_file_path, cron_output_file_path, base_path, log_dir,
                      file_base_name, cron_schedule) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (job_id, row['job_name'], row['cron_script_path'], row['cron_output_file_path'], row['csep_home'],
                    row['log_dir'], row['file_base_name'], row['cron_interval']))
      job_id += 1
  mysql_db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
  

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




