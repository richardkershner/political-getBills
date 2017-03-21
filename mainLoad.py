#python3 
from subprocess import call
import sys
import os
# get path based on input......  this creates a subfolder to the one working on
#mainDir = os.getcwd() + '/' + "politics_bills"
mainDir = os.getcwd() + '/'+sys.argv[1]
if not os.path.isdir(mainDir): os.mkdir(mainDir)

call(["python3", "getBillList.py",mainDir]) 
call(["python3", "getChangedBills.py",mainDir])

#session = '105th' 
#bill = '18'
#startPage = '21'
#stopPage = '22'
#call(["python3", "getBillList.py",mainDir, startPage, stopPage])
#call(["python3", "getBillTypes.py",mainDir, session, bill])
#call(["python3", "getBillTexts.py",mainDir, session, bill])

#python3 getBillTexts.py polTest
#subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, timeout=None, check=False, encoding=None, errors=None)

# maybe change the loads to path=   folder=  page=  ???