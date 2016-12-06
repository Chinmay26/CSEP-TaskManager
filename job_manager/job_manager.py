import os
import re

class JobManager:
  def __init__(self):
    #TO-DO
    #config setup
    self.ssh_client = None
    self.db_client = None

  def get_base_path_logs(self):
    #TO-DO
    # return path = '/home/csep/crontab_logs/'
    return './'

  def get_job_pids(self):
    '''
      Assumption - Each log file contains pid of cron job in its first line in the format
      [1] pid
		  Returns hash of file_name to job_pids
    '''
    pid_dict = {}
    log_file_dir = self.get_log_file_dir()
    for filename in os.listdir(log_file_dir):
      with open(filename, r) as f:
        read_data = f.readline().strip()
        try:
          k = re.search(r'\[\d\]? (\d)+', read_data)
          pid_dict[filename] = k.group(1)
        except AttributeError:
          #TO-DO raise exception or continue to next cron job?
          continue  
