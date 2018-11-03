import subprocess
from subprocess import  call
def print_currunt_dir():
   os_command = 'pwd'
   print os_command
   return_code = subprocess.call(os_command, shell=True)
   if return_code != 0:
     print return_code
     return return_code
print_currunt_dir()
