# Python3
import sys
import os
import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup

# ---- set up main directory ---------
# when calling this program, the arguements are folder(s) and main path
#       python3 getBillList.py myFolder  /home/politics   = /home/politics/myFolder
#       or python3 getBillList.py myFolder = curret_folder_Path/myFolder

class MainAccess:
   mainDir = ''
   def __init__(self, mainDir):
     self.mainDir = mainDir

  # --------- General File defs, and web calls

   def writeToFile(self, fileName, folderName, content):
     # basePath = '/home/richard/Documents/share/data/datapolitics/'#current code relies on this already existing
     if self.mainDir[-1:] != '/' and folderName[:1]  != '/':
       self.mainDir = self.mainDir + '/'
     fullFile = self.mainDir +  folderName 
     if not os.path.isdir(fullFile): os.mkdir(fullFile)
     fullFile += '/' + fileName     
     f = open(fullFile, 'w')
     chrIn = f.write(content)
     f.close()

   def writeToFileAppend(self, fileName, folderName, content):
     if self.mainDir[-1:] != '/' and folderName[:1] != '/':
       folderName = '/'  + folderName
     fullFile = self.mainDir +  folderName + '/' + fileName
     if not os.path.isdir(self.mainDir + folderName): os.mkdir(self.mainDir + folderName) 
     f = open(fullFile, 'a')
     chrIn = f.write(content+chr(13))
     f.close()

   def fileExist(self, fileName, folderName):
     fullFile = self.mainDir +  folderName + '/' + fileName
     if os.path.isfile(fullFile): return True
     return False
	 
   def getHTMLSoupPage(self, sourceURL, header):
     if header != '': data = requests.get(sourceURL, header)
     else: data = requests.get(sourceURL)
     soupPage = BeautifulSoup (data.content, 'html5lib')
     return soupPage
     
   def getFileText(self, folder, file):
     
     baseFile = self.mainDir
     if baseFile[-1:] != '/' and folder[:1] != '/' and baseFile != '':
       baseFile += '/'
     baseFile += folder
     if baseFile[-1:] != '/' and file[:1] != '/':
       baseFile += '/'
     baseFile += file
     f = open(baseFile, 'r')
     chrIn = f.read()
     f.close()
     return chrIn
	 	 
   def findAllInSoup(self, soupIn):
     #soupPage = BeautifulSoup (str(soupIn), 'html5lib')
     childNodes = soupIn.find_all(True)
     r = ''
     if len(childNodes) <= 1:# bottom of node tree
       if '<header>' in str(soupIn):
         r = ''
       else:
         r = soupIn.text + ' '
         print(r)
     else: # else, traverse node tree and append text of nodes
       for node in childNodes:
         child = self.findAllInSoup(node)

         r= r+' '+ child
         if node.tag == 'p' or node.tag == 'div': r = r + chr(13)
     return r
	 
   def stripHTMLFromPage(self, soupIn):
     strippedHTML = self.findAllInSoup(soupIn)
     #for tag in soupIn.find_all():
     #  print()
     #  print(tag.name)
     #  print(tag.get_text())
     return strippedHTML
   
   def readFromFile(self, fileName):
     f = open(fileName, 'r')
     chrIn = f.read()
     f.close()
     return chrIn

  # ---------------- specific to this data ----------------------
   def readDataList(self, billSession, billNum):
     # [0] = 115th_7   2=billTypes_date?,    3=
     billInfo = {}
     baseFile = self.mainDir + '/billList/' + billSession + '_' + billNum
     f = open(baseFile, 'r')
     chrIn = f.read()
     f.close()
     billStats = chrIn.split('\n')
     if billStats[1] == 'untouched':
       billInfo['billSession'] = billSession
       billInfo['billNumber'] = billNum
     else:
       for line in billStats:
        if line != '':
         data=line.split('=')
         billInfo[data[0]]=data[1]
     return billInfo

   def writeDataList(self, billSession, billNum, billStats):
     baseFile = self.mainDir + 'billList/' + billSession + '_' + billNum
     content = ''
     for item in billStats.items():
       content = content + item[0] + '=' + item[1] + chr(13)
     self.writeToFile(billSession + '_' + billNum,'/billList', content) 

   def getStartEndPagePull(self): 
     pullPage = 'https://www.congress.gov/search?q={%22source%22:%22legislation%22}&pageSort=latestAction:desc'
     soupPage = self.getHTMLSoupPage(pullPage, '')
     #<a class="last" href="/search?q=%7B%22source%22%3A%22legislation%22%7D&amp;pageSort=latestAction%3Adesc&amp;page=3991"><i></i><span>Last Page</span></a>
     hrefLast = soupPage.find('a', class_='last')['href'].split('page=')[1]
     pagesData = {'last_page':int(hrefLast)}  #3990  defaults to having not run if no file
     pagesData['lastRunPageCount'] = pagesData['last_page'] 
     #folder: pages    file:tracking    
     fileWPath = self.mainDir + '/pages/tracking'
     if os.path.isfile(fileWPath):
       data = self.readFromFile(fileWPath)
       lines = data.split('\n')
       for line in lines: #
         if len(line)>1:#filter blank lines
           col = line.split(';')
           pagesData[col[0]]=col[2]
           if col[1] == 'int':
             pagesData[col[0]]=int(col[2])
     #else:
        #self.savePagesTracking(pagesData)
     # to make sure no data is missed, +1. 
     if pagesData['lastRunPageCount'] != int(hrefLast):
       pagesData['last_page'] = pagesData['last_page'] + int(hrefLast) - pagesData['lastRunPageCount'] + 1
       pagesData['lastRunPageCount'] = int(hrefLast)
     #pagesData['lastRunPageCount'] = 3990
     #pagesData['last_page'] = 1
     #self.savePagesTracking(pagesData)
     return pagesData
     
   def savePagesTracking(self, dataLib): 
     content = ''
     for item in dataLib.items():
       if type(item[1]) is int: content = content + item[0] + ';int;' + str(item[1])+chr(13)
       else: content = content + item[0] + ';str;' + item[1]+chr(13)
     self.writeToFile('tracking', 'pages', content)
     
# test code for object
#ma = MainAccess('/home/richard/Documents/share/data/')
#ma.writeToFile('fileName.txt', 'folderName', 'test')