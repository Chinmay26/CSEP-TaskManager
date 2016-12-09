import subprocess

class SSH_Client:
  '''
     Simple SSH Client to eexcute commands on remote machine
  '''
  def __init__(self, host):
    self. host = host

  def execute_command(self, command, op_file, err_file):
    '''
       command = the command to be executed
       op_file = Contains the output of the command if successfully executed
       err_file = Contains error msgs based on command execution on remote machine
    '''
    try:
      result = subprocess.Popen(["ssh", self.host, command], shell=False, 
                                stdout=op_file, stderr=err_file)
    except SubprocessError:
      #TO-DO :Handle excpetion
      #should we retry ? or raise another custom exception
      pass
