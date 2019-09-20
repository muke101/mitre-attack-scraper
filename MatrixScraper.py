from bs4 import BeautifulSoup
import requests
import time
import csv
import os
import re

class pageScraper:
    def __init__(self, page):
        self.url = page
        self.page = requests.get(page)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')       
        self.pageName = self.soup.h1.get_text().strip()
        self.outputSoup = BeautifulSoup(open('template.html','rb'),'html.parser')
    
    
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
                text = []
                for content in tag.next_sibling.next_sibling.contents:
                    if content.string == None:
                        text.append(content.text) 
                    else:
                        text.append(content.string)
                pt3Dict[tag.contents[0]] = re.sub('\[\d\]','', ''.join(text))
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

    def descBodyInserter(self): 
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

        newSoup = BeautifulSoup("<p><strong>ID</strong>: <a href="+self.url+">"+cardDict['ID']+"</a></p>",'html.parser')
        startPosition.insert_before(newSoup)
        del cardDict['ID']

        for key in cardDict.keys():
            newSoup = BeautifulSoup("<p><strong>"+key+"</strong>: "+cardDict[key]+"</p>","html.parser")
            startPosition.insert_before(newSoup) 
                

    def build(self):
        self.pt3Inserter()
        self.descBodyInserter()
        self.cardInserter()

        fileName = re.sub('/', '^', self.pageName+'.html') #can't write file names with slashes in them, replacing with unique character to make parsing it out easier later
        output = open(fileName, 'w')
        output.write(re.sub('</ac:layout>', '', str(self.outputSoup)))
        output.close()
        os.system('echo \'</ac:layout>\' >> \''+fileName+'\'') #dirty hack - please ignore

def webScraper():
    soup = BeautifulSoup(open('windows','rb'), 'html.parser')       
    c = 0
    for row in soup.tbody.children:
        if row != '\n':
            for box in row:
                if box != '\n' and box.a != None:
                    print('Writing ' + box.a['href'].split('/')[-1])
                    pageScraper('https://attack.mitre.org'+box.a['href']).build()
                    c+=1
                    print('page '+str(c)+' written')
                    time.sleep(5)
webScraper()
