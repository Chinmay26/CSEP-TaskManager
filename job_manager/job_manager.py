import os
import re

class JobManager:
  def __init__(self):
    #TO-DO
    #config setup
    self.ssh_client = None
    self.db_client = None

  def get_log_file_dir(self):
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
          k = re.search(r'\[\d\]? (\d+)', read_data)
          pid_dict[filename] = k.group(1)
        except AttributeError:
          #TO-DO raise exception or continue to next cron job?
          continue  

    return pid_dict

  def get_active_cron_jobs(self):
    '''
       #Run ps -f -p 22564,22914 on csep machine to check running jobs and full output format
       Run ps -o pid -p 22564,22914 on csep machine to check running jobs
    '''
    pid_dict = self.get_job_pids()
    pids = list(pid_dict.values())
    command = "ps -o pid -p " + ','.join(map(str, pids))
    #TO-DO Add below files in config settings
    op_file = f.open('./ssh_output', 'w+')
    err_file = f.open('./ssh_error', 'w+')
    self.ssh_client.execute_command(command, op_file, err_file)
    #Parse output file to check if there are any active crons
    active_job_pids = []
    for line in op_file:
      line = line.strip()
      #Ignore Header
      if "PID" in line:
        continue
      else:
        active_job_pids.append(k)
    op_file.close()
    err_file.close()
    return active_job_pids






