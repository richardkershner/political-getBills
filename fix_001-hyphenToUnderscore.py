# Python3
import sys
import os
from subprocess import call
import requests
from generalFileCommands import MainAccess

mainDir = sys.argv[1]
if mainDir[-1:] != '/': mainDir = mainDir + '/'
folder = mainDir + 'bills'
#for all files in billList
print(folder)
for fileName in os.listdir (folder):
  print(fileName)
  fullFile1 = folder + '/' + fileName
  fullFile2 = folder + '/' + fileName.replace('-','_')
  os.rename(fullFile1, fullFile2)