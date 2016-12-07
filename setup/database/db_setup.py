'''
Script to setup DB tables for CSEP Job Manager
'''

import sqlite3 as db
import csv

db_connection = db.connect('../../data/csep_job_monitor.db') # TO-DO Read this from a settings a file

with db_connection:
  c = db_connection.cursor()
  c.execute('''CREATE TABLE JobManager
               (id INT primary key, version text, base_location text)''')

  c.execute('''CREATE TABLE Job
               (id INT primary key, job_name text unique, script_file_path text, cron_output_file_path text, base_path text, 
                log_dir text, file_base_name text, cron_schedule text)''')

  c.execute('''CREATE TABLE JobHistory
               (id INT, status text, start_time text, end_time text, log_file_path text unique)''')

  #Setup metadata of jobs
  with open('./csep_job_metadata.csv', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    job_id = 1
    for row in csv_reader:
      c.execute('''INSERT INTO Job(id, job_name, script_file_path, cron_output_file_path, base_path, log_dir,
                      file_base_name, cron_schedule) VALUES(?,?,?,?,?,?,?,?)''',
                    (job_id, row['job_name'], row['cron_script_path'], row['cron_output_file_path'], row['csep_home'], 
                    row['log_dir'], row['file_base_name'], row['cron_interval']))
      job_id += 1


  db_connection.commit()

