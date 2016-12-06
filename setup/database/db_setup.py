'''
Script to setup DB tables for CSEP Job Manager
'''

import sqlite3 as db

db_connection = db.connect('csep_job_monitor.db') # TO-DO Read this from a settings a file

with db_connection:
  c = db_connection.cursor()
  c.execute('''CREATE TABLE JobManager
               (id INT, version text, base_location text)''')

  c.execute('''CREATE TABLE Job
               (id INT, log_file_base_path text, name text, run_interval text)''')

  c.execute('''CREATE TABLE JobHistory
               (id INT, status text, start_time text, end_time text, log_file_path text)''')


	#TO-DO
  #Add Job description entries

