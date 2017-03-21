# Python3
import sys
import os
from subprocess import call
import requests
from generalFileCommands import MainAccess

# became unnecessary as bills where read with white space at the top
mainDir = sys.argv[1]
dataStorage = MainAccess('')

if mainDir[-1:] != '/': mainDir = mainDir + '/'
folderBills = mainDir + 'billList'
print(folderBills)
folderChanged = 'billsChanged'

for fileName in os.listdir (folderBills):
  # note 100th and less congress is NOT available in digital version
  number = int(fileName.split('_')[0][:-2])
  if not number <= 100:
    if 'untouched' in dataStorage.getFileText(folderBills, fileName):
      dataStorage.writeToFile(fileName, folderBills, fileName)