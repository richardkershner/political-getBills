# Python3
import sys
import os
from subprocess import call
import requests
from generalFileCommands import MainAccess

# became unnecessary as bills where read with white space at the top
mainDir = sys.argv[1]
if mainDir[-1:] != '/': mainDir = mainDir + '/'
folder = mainDir + 'bills'
#for all files in billList
print(folder)
for fileName in os.listdir (folder):
  pass