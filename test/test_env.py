# https://stackoverflow.com/questions/8365394/set-environment-variable-in-python-script

import os
import subprocess
import sys

os.environ['HOME'] = "my_path" # visible in this process + all children

                      
if 'HOME' in os.environ:
    print('HOME environment variable is already defined. Value =', os.environ['HOME'])
else:
    print('HOME environment variable is not defined.')