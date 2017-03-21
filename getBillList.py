# Python3
import sys
import os
import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from generalFileCommands import MainAccess

mainDir = sys.argv[1]
dataStorage = MainAccess(mainDir)
pageData = dataStorage.getStartEndPagePull()
page = 1 # default
pageEnd= pageData['last_page']
if len(sys.argv)>2:
  page = int(sys.argv[2])
  pageEnd = int(sys.argv[3])


def getCongressBillBilltype(searchResultMain):
   heading = searchResultMain.find('span', class_='result-heading')
   congress = ''
   bill = ''
   billType = ''
   congressTemp = str(heading).split('/')
   if len(congressTemp) >7:#blank 1,7 and 2 =www.congress.gov
      congress = congressTemp[4].split('-')[0] #114th-congress
      bill = congressTemp[6].split('?r')[0]#337
   else: congress = 'error' + str(heading)
   return congress, bill
   
def getBillList():
  global page 
  global pageEnd
  global dataStorage
  httpActionsAll = "https://www.congress.gov/search?q={%22source%22:%22legislation%22}&pageSort=latestAction:desc&page="   
  while page < pageEnd:# as of running this, there are 3985 pages with 100 per page
    hPage = httpActionsAll + str(page)
    dataStorage.writeToFileAppend('page.txt', 'pages', hPage + chr(13))
    soupPage = dataStorage.getHTMLSoupPage(hPage, '')
    soupSearchSection = soupPage.find('ol', class_='basic-search-results-lists expanded-view')
    searchResults = soupSearchSection.find_all('li', class_='expanded')
    for result in searchResults:# this returns bill actions/ammendments/etc.
      congress, bill = getCongressBillBilltype(result)
      baseText = congress + '_' + bill
      postText = baseText + chr(13) + 'untouched'
      if not dataStorage.fileExist(baseText, 'billList'):
        dataStorage.writeToFile(baseText, 'billList', postText)
    #dataStorage.writeToFile(baseText, 'billList', postText)
    dataStorage.writeToFile(baseText, 'billsChanged', baseText)  
    page += 1
	   
try:
  getBillList()
  pageData['last_page']=1
  if len(sys.argv)<2:
    dataStorage.savePagesTracking(pageData)
except Exception as e:
  fileName =  '_page_'+str(page)
  folderName = 'errors'
  content = 'error in ' + str(sys.modules[__name__])+ ': ' +  str(e)
  dataStorage.writeToFile(fileName, folderName, content)