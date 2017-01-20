import subprocess
import io
import re
from db_client import DB_Client
from datetime import datetime,timedelta

FILE_SEPARATOR = '/'
MONTH_LOG_SEPARATOR = '_'
LOG_FILE_DATE_SEPARATOR = '-'

class LogParser:
  ''' Base Class to parse cron log files
  '''
  def __init__(self, start_time, end_time):
    #mapping between job name and job_details
    self.cron_job_meta = {}
    #mapping between job id and job name
    self.job_id_dict = {}
    self.db = DB_Client()
    results = self.db.execute_sql_command('select * from jobs')
    for job in results:
      self.cron_job_meta[job['job_name']] = job
      self.job_id_dict[job['id']] = job['job_name']
    #print('job_meta', self.cron_job_meta)
    #print('RESULTS', self.job_id_dict)
    self.start_time = start_time
    self.end_time = end_time

  def execute_command(self, command):
    '''
       command = the command to be executed
       op_file = Contains the output of the command if successfully executed
       err_file = Contains error msgs based on command execution on remote machine
    '''
    try:
      process = subprocess.Popen(command, shell=True, 
                                stdout=subprocess.PIPE)
      return process
    except subprocess.CalledProcessError:
      #TO-DO :Handle excpetion
      #should we retry ? or raise another custom exception
      pass

  def get_log_paths(self, job_name, start_time, end_time):
    '''
       For a given job and date range, get a month-wise dict of cron log file to be grepped
       {'2016-10': '/home/csep/operations/dispatcher/logs/2016_10/dailyANSS1985_2016-10-*'}
    '''
    job_metadata = self.cron_job_meta[job_name]
    parent_dir = job_metadata['base_path'] + job_metadata['log_dir']

    #This will be the list of file paths to search
    file_dict = {}
    month_directory = []
    #since logs are stored month-wise
    if start_time.year == end_time.year :
      if (start_time.month == end_time.month):
        month_directory.append(start_time)
      else:
        #Add all timestamps from start_time to end_time
        #Get all first days of the month from start_time and end_time
        st_first_day = start_time.replace(day=1)
        et_first_day = end_time.replace(day=1)
        temp_date = et_first_day

        while temp_date != st_first_day:
          month_directory.append(temp_date)
          temp_date = temp_date - timedelta(days=1)
          temp_date = temp_date.replace(day=1)

        month_directory.append(temp_date)
    else:
      #Add all timestamps from start_time to end_time
      #Get all first days of the month from start_time and end_time
      st_first_day = start_time.replace(day=1)
      et_first_day = end_time.replace(day=1)
      temp_date = et_first_day

      while temp_date != st_first_day:
        month_directory.append(temp_date)
        temp_date = temp_date - timedelta(days=1)
        temp_date = temp_date.replace(day=1)

      month_directory.append(temp_date)

    for m in month_directory:
      cur_dir = parent_dir
      cur_dir += (FILE_SEPARATOR + str(m.year) + MONTH_LOG_SEPARATOR + str(m.month))
      file_meta_path = cur_dir + FILE_SEPARATOR + job_metadata['file_base_name'] + str(m.year) + \
                       LOG_FILE_DATE_SEPARATOR + str(m.month) + LOG_FILE_DATE_SEPARATOR
      month = str(m.year) + LOG_FILE_DATE_SEPARATOR + str(m.month)
      file_dict[month] = file_meta_path
    return file_dict

  def get_log_files(self, dir_list):
    '''
       Get list of log files from dir_list, ignores directories
       Ex:  i/p ['/home/csep-op/operations/dispatcher/logs/2016_10/dailyANSS1985_2016-10-4-*']
            o/p [file1, file2,...]
    '''
    #command = 'ls -p file1,file*'
    command = "ls -p " + ' '.join(map(str, dir_list))
    #command += "*"

    proc = self.execute_command(command)
    log_files = []
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
      log_files.append(line.strip())
    return log_files

  def get_db_entries(self, job_data, start_time, end_time):
    command = "select log_file_path from job_history where job_id = %s and start_time > %s and end_time < %s"
    st = start_time.strftime('%Y-%m-%d %H:%M:%S')
    et = end_time.strftime('%Y-%m-%d %H:%M:%S')
    query_t = (job_data['id'] ,st, et)

    results = self.db.execute_sql_command(command, query_t)
    db_files = []
    for lg in results:
      db_files.append(lg['log_file_path'])
    return db_files

  def get_cron_log_files_for_job(self, job_name, start_time, end_time):
    ''' For given job, get a dict of cron log files between the given set of dates
       Assumes start_time and end_time are date time objects
       {'2016-10-21': [log_file_1, log_file_2, log_file_3], '2016-10-22': [log_file_1]}
    '''
    lp = self.get_log_paths(job_name, start_time, end_time)
    lpv = list(lp.values())
    #Add meta-character to input list
    lpv = [ i+'*' for i in lpv ]
    #print('meta_month_list', lpv)
    #TO-DO Filter files from start date to end date
    log_files = self.get_log_files(lpv)
    #print('log_files11', log_files)
    return log_files

  def filter_logs_by_time_stamp(self, job_name, logs, start_time, end_time):
    '''
       Given log files of the month, filter files based on start time and end time
    '''
    job_metadata = self.cron_job_meta[job_name]
    base_name = job_metadata['file_base_name']
    log_files = []
    for file_path in logs:
      pos = file_path.find(base_name)
      if pos != -1:
        ts = file_path[pos+len(base_name):]
        #ts = '2016-12-9-001001'
        dt = datetime.strptime(ts, "%Y-%m-%d-%H%M%S")
        if start_time <= dt and dt <= end_time:
          log_files.append(file_path)
    return log_files

  def get_job_ids(self, job_data):
    job_ids = []
    for job_name, job_details in job_data.items():
      job_ids.append(job_details['id'])
    return job_ids

  def get_file_metadata(self, files):
    #command = 'ls -al --full-time'
    command = "ls -l --full-time " + ' '.join(map(str, files))
    #TO-DO Add below files in config settings
    proc = self.execute_command(command)
    return proc

  def create_job_history_db_entries(self, log_entries):
    command = 'insert ignore into job_history(job_id,status,start_time,end_time,log_file_path)'
    command += 'values("{job_id}","{status}","{start_time}","{end_time}","{log_file_path}"")'.format(job_id=log_entries[0]['job_id'], 
                status=log_entries[0]['status'], start_time=log_entries[0]['start_time'], end_time=log_entries[0]['end_time'],
                log_file_path=log_entries[0]['file_path'])

    for entry in log_entries[1:]:
      command += ',("{job_id}","{status}","{start_time}","{end_time}","{log_file_path}")'.format(job_id=entry['job_id'], 
                status=entry['status'], start_time=entry['start_time'], end_time=entry['end_time'],
                log_file_path=entry['file_path'])

    print('Creating Database entries\n', command)
    results = self.db.execute_sql_command(command)
    return results

  def get_job_name_from_log_file(self, log):
    for job_name,job_details in self.cron_job_meta.items():
      if job_details['file_base_name'] in log:
        return job_name
    return None

  #FIX-THIS
  #Use base-file-name and extract timestamp
  def extract_time_from_file_name(self, file_name):
    start_time_stamp = file_name.split('_')[-1].split('-')
    seconds = start_time_stamp[-1]
    if len(seconds) != 6:
      return None
    formatted_seconds_timestamp = seconds[0:2] + ":" + seconds[2:4] + ":" + seconds[4:]
    t1 = '-'.join(start_time_stamp[:-1])
    st = t1 + ' ' + formatted_seconds_timestamp
    return st

  def build_log_entries(self, log_files, status):
    proc = self.get_file_metadata(log_files)
    log_entries = []
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
      line = line.strip()
      file_data = line.split(' ')
      log_details = {}
      log_details['file_path'] = file_data[-1]
      file_name = log_details['file_path'].split('/')[-1]
      job_name = self.get_job_name_from_log_file(file_name)
      if job_name is None:
        continue
      log_details['start_time'] = self.extract_time_from_file_name(file_name)
      if log_details['start_time'] is None:
        continue
      log_details['end_time'] = file_data[-4] + ' ' + file_data[-3]

      log_details['job_id'] = self.cron_job_meta[job_name]['id']
      log_details['status'] = status
      log_entries.append(log_details)
    return log_entries
    

  def parse_new_cron_output(self, new_files):
    #command = 'grep -l "SUCCESS"'
    command = "grep -l 'SUCCESS' " + ' '.join(map(str, new_files))
    #TO-DO Add below files in config settings
    proc = self.execute_command(command)
    success_cron_logs = []
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
      success_cron_logs.append(line.strip())

    failure_cron_logs = set(new_files) - set(success_cron_logs)
    log_entries = []
    success_entries = self.build_log_entries(success_cron_logs, 'SUCCESS')
    failure_entries = self.build_log_entries(list(failure_cron_logs), 'FAILURE')
    log_entries.extend(success_entries)
    log_entries.extend(failure_entries)
    self.create_job_history_db_entries(log_entries)


  def get_results_from_db(self, start_time, end_time):
    '''
       Get DB entries for given time range and given jobs
    '''
    command = "select * from job_history where job_id in %s and start_time > %s and end_time < %s"
    st = start_time.strftime('%Y-%m-%d %H:%M:%S')
    et = end_time.strftime('%Y-%m-%d %H:%M:%S')
    job_ids = tuple(self.get_job_ids(self.cron_job_meta))
    query_t = (job_ids, st, et)
    results = self.db.execute_sql_command(command, query_t)
    return results

  def parse(self):
    '''
       Parse the cron log files within the given time-range
    '''
    remain_files = []
    for job_name, job_details in self.cron_job_meta.items():
      
      log_files = self.get_cron_log_files_for_job(job_name, self.start_time, self.end_time)
      #print('log_files', log_files)
      logs = self.filter_logs_by_time_stamp(job_name, log_files, self.start_time, self.end_time)
      print('Current log files :\n', logs)

      #Get log files from DB
      db_files = self.get_db_entries({'id': job_details['id']}, self.start_time, self.end_time)
      print('Log entries in DB :\n', db_files)
      diff = set(logs) - set(db_files)
      print('Log file entries to be created : \n', diff)
      remain_files.extend(list(diff))

    if len(remain_files) > 0:
      #Parse these files and create DB entries
      #print('remain', remain_files)
      self.parse_new_cron_output(remain_files)

    
    #change start time to start of day
    st = self.start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    result = self.get_results_from_db(st, self.end_time)
    response = self.build_response(result, self.start_time, self.end_time)
    #print(type(result[0]),'\nRESPONSE', response)
    return response


  def build_response(self, result, start_time, end_time):
    response = {'jobs': {}, 'days': []}
    #Add all timestamps from start_time to end_time
    start_date = start_time.date()
    end_date = end_time.date()
    temp_date = start_date

    while temp_date != end_date:
      response['days'].append(temp_date)
      temp_date = temp_date + timedelta(days=1)

    for job_name in self.cron_job_meta.keys():
      response['jobs'][job_name] = {}

    for db_entry in result:
      job_id = db_entry['job_id']
      job_name = self.job_id_dict[job_id]

      result_date = db_entry['start_time'].date()
      if result_date in response['jobs'][job_name]:
        if db_entry['status'] == 'SUCCESS' and response['jobs'][job_name][result_date]['status'] == 'FAILURE':
          response['jobs'][job_name][result_date] = db_entry
      else:
        response['jobs'][job_name][result_date] = db_entry

    return response
