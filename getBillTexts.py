# Python3
import sys
import os
import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from generalFileCommands import MainAccess

mainDir = sys.argv[1]
session =  sys.argv[2]#'115th'  
bill = sys.argv[3]#'7'

dataStorage = MainAccess(mainDir)

def getBillTexts(billInfo):#-------------------
 if billInfo['texts'].strip() != '':
  global dataStorage
  sessionNum = billInfo['billSession']
  billNum = billInfo['billNumber']
  billURL = 'https://www.congress.gov/bill/'+billInfo['billSession'] + '-congress/house-bill/' +billInfo['billNumber'] +'/text'
  for v in billInfo['texts'].split(' '):
    v=v.strip()
    if 'not loaded yet' == billInfo[v+'-status'] or 'bill has not been posted yet' == billInfo[v+'-status']:
     #https://www.congress.gov/bill/114th-congress/house-bill/10/text/rds
     billURL = 'https://www.congress.gov/bill/'+sessionNum + '-congress/house-bill/' +billNum+'/text/'+v # 6431/text/ih eh rds enr
	 #house-bill/7/text/eh?format=txt  
     soupBillPage = dataStorage.getHTMLSoupPage(billURL, '')
     soupBillText = dataStorage.getHTMLSoupPage(billURL + '?format=txt', '').find('pre', id='billTextContainer')
     soupBillMain =  None
     soupTextTypes =  None
     soupHTMLNew =  None
     soupMain = None
     soupPreBillTextContainerPage =  None
     soupBillGeneratedHTMLContainer = None
     if soupBillPage != None:
       soupBillMain = soupBillPage.find('div', id='main') 
       soupTextTypes = soupBillPage.find('h3', class_='texgtFormatsHeader')
       soupHTMLNew = soupBillPage.find('a', text='XML/HTML (new window)')
       soupPreBillTextContainerPage = soupBillPage.find('pre', id='billTextContainer')
       if soupBillMain != None: 
         soupBillGeneratedHTMLContainer = soupBillMain.find('div', class_='generated-html-container')
         if soupBillGeneratedHTMLContainer != None: 
           soupBillGeneratedHTMLContainer.find('body')
       soupMain = soupBillPage.find(id="main")
     fileName = sessionNum+'_'+billNum +'_'+v
     if 'bill has not been posted yet' in str(soupMain):
        billInfo[v+'-status']='not available yet'
     elif 'Reserved Bill - Reserved'  in str(soupBillPage):
       #  reserved bill number but not used.
       billInfo['reserved'] = 'Reserved Bill - Reserved'
       billInfo['texts']=''
       del billInfo[v +'-ref']
       del billInfo[v +'-status']
     elif soupBillText != None:
        # Main pull of most bills
        dataStorage.writeToFile(fileName, 'bills', soupBillText.text)
        billInfo[v+'-status']='processed by soupBillText (TEXT version)'
     elif soupBillGeneratedHTMLContainer != None: #pull from this generated page	 
        # most likely never used
        billText = dataStorage.stripHTMLFromPage(soupBillGeneratedHTMLContainer)
        dataStorage.writeToFile(fileName, 'bills', billText + '*** a ***')
        billInfo[v+'-status']='GeneratedHTMLContainer'
     elif soupHTMLNew != None: #if the HTML exists as a new page
        # most likely never used
        LinkHTMLFullPage =  'https://www.congress.gov' +  soupHTMLNew.get('href')
        soupBillText = dataStorage.getHTMLSoupPage(LinkHTMLFullPage, '')#.getText(separator=u' ')
        billText = dataStorage.stripHTMLFromPage(soupBillText)
        dataStorage.writeToFile(fileName, 'bills', billText+ '*** B ***')
        billInfo[v+'-status']='processed by HTMLNewPage'
     elif soupPreBillTextContainerPage != None:
        # most likely never used
        billText = dataStorage.stripHTMLFromPage(soupPreBillTextContainerPage)
        dataStorage.writeToFile(fileName, 'bills', billText+ '*** C ***')
        billInfo[v+'-status']='processed by preBillTextContainer'
     else: #--- pull text here -----
        print('something is probably wrong. Like bill not available')
        # note in 104th-congress/house-bill/4456
        #   in the 104th, there are about 20 bills that disappeared but are in the 
        #   list pull.
        pnt = len(soupMain.contents) - 1
        billText = str(soupMain.contents[pnt].text.strip())
        dataStorage.writeToFile(fileName, 'bills', billText+ '*** D ***')
        billInfo[v+'-status']='processed by allElse'
		
try:
  billStats = dataStorage.readDataList(session, bill)
  getBillTexts(billStats)
  dataStorage.writeDataList(session, bill,billStats)
except Exception as e:
  fileName = session +'_'+bill
  folderName = 'errors'
  content = 'error in ' + str(sys.modules[__name__])+ ': ' +  str(e)
  dataStorage.writeToFile(fileName, folderName, content)

# ------------------------ Notes ---------------------------
#  note pl for public law              Became Public Law
# enr enrolled bill (to president)     Presented to President. 
# eas engrosssed ammendment Senate  
# rfs referred in senate               
# rh reported in house
# eh engrossed in house
# ih intorduced in house
# [ih, is, ath, ats, cph, cps, eah, eas, pch, pcs, rfh, rfs, rh, rs, eh, es, enr, pl]
#  and now, pl 
#https://www.congress.gov/bill/115th-congress/house-bill/7' +billNum+'/text/ih 