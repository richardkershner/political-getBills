# Python3
import sys
import os
from subprocess import call
import requests
from generalFileCommands import MainAccess

mainDir = sys.argv[1]
dataStorage = MainAccess(mainDir)#not necessary for the below

if mainDir[-1:] != '/': mainDir = mainDir + '/'
folder = mainDir + 'billsChanged'

for fileName in os.listdir (folder):
  #print (folder + '/'+fileName)
  parts = fileName.split('_')
  session = parts[0]
  bill = parts[1]
  #print(session, bill)
  call(["python3", "getBillTypes.py",mainDir, session, bill])
  call(["python3", "getBillTexts.py",mainDir, session, bill])
  text = dataStorage.getFileText('billList', fileName)
  if not 'not loaded yet' in text and 'not available yet' not in text:
    os.remove(folder + '/'+fileName)
  
