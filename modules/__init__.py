import os
print "Printing from the init at module {}".format(os.getcwd())

import os
import subprocess
print os.getcwd()
proc1 = subprocess.Popen(['ps','-ef'],stdout=subprocess.PIPE)
proc2a = subprocess.Popen(['grep','compass'],stdin=proc1.stdout,
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE)
proc2 = subprocess.Popen(['grep','-v', 'grep'],stdin=proc2a.stdout,
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE)
proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
out,err=proc2.communicate()
if not out:
    print "nothing running"
    proc3 = subprocess.Popen(['compass','watch',os.path.join(os.getcwd(),'applications','web2py_start_2016','static')])
print('out: {0}'.format(out))
print('err: {0}'.format(err))
