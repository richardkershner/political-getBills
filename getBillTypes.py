# Python3
import sys
import os
import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from generalFileCommands import MainAccess
import datetime

mainDir = sys.argv[1]
session =  sys.argv[2]#'115th'  
bill = sys.argv[3]#'7'

dataStorage = MainAccess(mainDir)

def getDataVersions(billStats):#-------------------
  global dataStorage
  sessionNum = billStats['billNumber']
  billNum = billStats['billSession']
  billURL = 'https://www.congress.gov/bill/'+billStats['billSession'] + '-congress/house-bill/' +billStats['billNumber'] +'/text'
  soupBillPage = dataStorage.getHTMLSoupPage(billURL, '')
  soupMain = soupBillPage.find(id="main")
  soupSelects = soupBillPage.find(id='textVersion')
  versionsListed = {}
  if soupSelects != None: 
    soupOpts = soupSelects.find_all('option')
    if len(soupOpts) == 0: #means that ih is active and not shown under versions
          versionsListed['ih']='no versions listed, default ih only' 
    else: # -------- this comes up with a no text version, xml only ?????
         for option in soupOpts: 
           versionsListed[option.get('value')]=option.text
  else:
    versionsListed['ih']='no versions listed, default ih only'
  strBillList = ''
  if 'texts' not in billStats: billStats['texts']='' 
  for item in versionsListed.items():
    billStats[item[0]+'-ref']=item[1]
    if item[0] not in billStats['texts']:
      billStats[item[0]+'-status']='not loaded yet'
    strBillList= strBillList + ' ' + item[0]
    strBillList = strBillList.strip()
  billStats['texts']=strBillList
  return billStats

#---------------- test scripts ----------------------------------  
try: 
  billStats = dataStorage.readDataList(session, bill)
  billStats = getDataVersions(billStats)

  dataStorage.writeDataList(session, bill,billStats)
  folderName = 'billsChanged'
  content = str(datetime.datetime)
  dataStorage.writeToFile(session + '_' + bill, folderName, content)
    
    #dataStorage.writeToFile(session + '_' + bill, billsNeedLoading, content)
  
except Exception as e:
  fileName =  +'_type:'+session + '_' + bill
  folderName = 'errors'
  content = 'error in ' + str(sys.modules[__name__])+ ': ' +  str(e)
  dataStorage.writeToFile(fileName, folderName, content)
# notes ------------------------------------------------------------
#https://www.congress.gov/bill/115th-congress/house-bill/7' +billNum+'/text/ih
#  note pl for public law              Became Public Law
# enr enrolled bill (to president)     Presented to President. 
# eas engrosssed ammendment Senate  
# rfs referred in senate               
# rh reported in house
# eh engrossed in house
# ih intorduced in house
# [ih, is, ath, ats, cph, cps, eah, eas, pch, pcs, rfh, rfs, rh, rs, eh, es, enr, pl]
#  and now, pl