from bs4 import BeautifulSoup
import requests
import time
import csv
import os
import re

class pageScraper:
    def __init__(self, page):
        #self.page = requests.get(page)
        self.soup = BeautifulSoup(page, 'html.parser')       
        self.pageName = self.soup.h1.get_text().strip()
        self.outputSoup = BeautifulSoup(open('source2.html','rb'),'html.parser')
        self.page = 'www.mitreattack.com'
    
    
    def cardScraper(self):
        cardDict = {}
        cardRemoval = ['Version', 'Contributors', 'CAPEC ID']
        for tag in self.soup.find_all(class_='card-data'):
            strings = tag.strings
            key = re.sub(r'[^\x00-\x7f]|:',r'', next(strings))
            if key != ' ': 
                cardDict[key] = [i for i in strings][0].strip(' :') 
        for entry in cardRemoval:
            try:
                del cardDict[entry]
            except KeyError:
                pass
        return cardDict
                
    def pt3Scraper(self):
        pt3Dict = {}
        pt3Removal = ['references', 'examples'] 
        for tag in self.soup.find_all(class_='pt-3'):
            if tag['id'] not in pt3Removal:
                pt3Dict[tag.contents[0]] = re.sub('\[\d\]','',tag.next_sibling.next_sibling.contents[0]) 
        return pt3Dict
    
    def descBodyScraper(self): 
        descDict = {} 
        firstHeader = True
        paragraphs = []
        for tag in self.soup.find(class_='col-md-8 description-body').contents:
            if tag != '\n':
                if tag.name != 'h3':
                    paragraphs.append(re.sub('\[\d\]','',tag.get_text())+' ')
                elif firstHeader == True:
                    descDict[self.pageName] = ''.join(paragraphs)
                    firstHeader = False
                    currentHeader = tag.get_text().strip()
                    paragraphs = []
                else:
                    descDict[currentHeader] = ''.join(paragraphs)
                    currentHeader = tag.get_text().strip()
                    paragraphs = []
        if firstHeader == True:
            descDict[self.pageName] = ''.join(paragraphs)    
        else:
            descDict[currentHeader] = ''.join(paragraphs)
        return descDict
        

    def pt3Inserter(self):
        contentList = ['Mitigation', 'Detection']
        pt3Dict = self.pt3Scraper()

        c = 0
        for tag in self.outputSoup.tbody.children:
            if tag != '\n':
                tag.contents[1].p.string = pt3Dict[contentList[c]]
                c+=1

    def descBodyInserter(self): #TODO: test if insert_after is actually the inteded way to do this
        descDict = self.descBodyScraper()

        self.outputSoup.find('p').string = descDict[self.pageName] 
        del descDict[self.pageName]

        for header in descDict.keys():
            newTag = self.outputSoup.new_tag("h3") 
            newTag.string = header
            self.outputSoup.p.insert_after(newTag)

        for header in self.outputSoup.find_all('h3'):
            newTag = self.outputSoup.new_tag("p")
            newTag.string = descDict[header.get_text()]
            header.insert_after(newTag)

    def cardInserter(self): 
        cardDict = self.cardScraper()
        startPosition = self.outputSoup.find('h1').next_sibling

        newSoup = BeautifulSoup("<p><strong>ID</strong>: <a href="+self.page+">"+cardDict['ID']+"</a></p>",'html.parser')
        startPosition.insert_before(newSoup)
        del cardDict['ID']

        for key in cardDict.keys():
            newSoup = BeautifulSoup("<p><strong>"+key+"</strong>: "+cardDict[key]+"</p>","html.parser")
            startPosition.insert_before(newSoup) 
                

    def build(self):
        self.pt3Inserter()
        self.descBodyInserter()
        self.cardInserter()

        fileName = self.pageName+'.html'
        output = open(fileName, 'w')
        output.write(re.sub('</ac:layout>', '', str(self.outputSoup)))
        output.close()
        os.system('echo \'</ac:layout>\' >> \''+fileName+'\'')

def webScraper():
    file1 = open('T1028','rb')
    file2 = open('T1044','rb')
    soup = BeautifulSoup(open('windows','rb'), 'html.parser')       
    for row in soup.tbody.children:
        if row != '\n':
            for box in [file1, file2]:
                #if box != '\n' and box.a != None:
                pageScraper(box).build()
                #pageScraper('https://attack.mitre.org'+box.a['href']).build()
                print('page written')
                    #time.sleep(5)
webScraper()
