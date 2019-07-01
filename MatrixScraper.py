from bs4 import BeautifulSoup
import requests
import time
import csv
import os
import re

class pageScraper:
    def __init__(self, page):
        #page = requests.get(page)
        self.soup = BeautifulSoup(page, 'html.parser')       
        self.pageName = self.soup.h1.get_text().strip()
        self.cardRemoval = ['Version', 'Contributors:\xa0']
        self.pt3Removal = ['references', 'examples'] 
    
    
    def cardScraper(self):
        cardDict = {}
        for tag in self.soup.find_all(class_='card-data'):
            strings = tag.strings
            key = next(strings) #TODO: stirp off random hex's
            if key != ' ': 
                cardDict[key] = [i for i in strings][0].strip(' :') 
        for entry in self.cardRemoval:
            try:
                del cardDict[entry]
            except KeyError:
                pass
        return cardDict
                
    def pt3Scraper(self):
        pt3Dict = {}
        for tag in self.soup.find_all(class_='pt-3'):
            if tag['id'] not in self.pt3Removal:
                pt3Dict[tag.contents[0]] = re.sub('\[\d\]','',tag.next_sibling.next_sibling.contents[0]) 
        return pt3Dict
    
    def descBodyScraper(self): 
        descDict = {} 
        firstHeader = True
        for tag in self.soup.find(class_='col-md-8 description-body').contents:
            if tag != '\n':
                paragraphs = []
                if tag.name != 'h3':
                    paragraphs.append(re.sub('\[\d\]','',tag.get_text()))
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
                tag.contents[3].p.string = pt3Dict[contentList[c]]
                c+=1

    def descBodyInserter(self): #TODO: test if insert_after is actually the inteded way to do this
        descDict = self.descBodyScraper()

        self.outputSoup.find('p').string = descDict[self.pageName] 
        del descDict[self.pageName]

        for header in descDict.keys():
            newTag = self.outputSoup.new_tag("h3") 
            newTag.string = header
            self.outputSoup.p.insert_before(newTag)

        for header in self.outputSoup.find_all('h3'):
            newTag = self.outputSoup.new_tag("p")
            newTag.string = descDict[header.get_text()]
            header.insert_after(newTag)

    def cardInserter(self):
        pass

    def build(self, csv, html):
        cardDict = self.cardScraper()

        fileName = self.pageName+'.html'
        os.system('cp source.html \''+fileName+'\'')
        self.outputSoup = BeautifulSoup(open(fileName,'rb'),'html.parser')

        self.pt3Inserter()
        self.descBodyInserter()

def webScraper():
    file1 = open('T1028','rb')
    file2 = open('T1044','rb')
    csvfile = csv.writer(open('output.csv', 'w'), delimiter=',')
    htmlfile = open('output.html', 'w')
    soup = BeautifulSoup(open('windows','rb'), 'html.parser')       
    for row in soup.tbody.children:
        if row != '\n':
            for box in [file1, file2]:
                #if box != '\n' and box.a != None:
                pageScraper(box).build(csvfile, htmlfile)
                #pageScraper('https://attack.mitre.org'+box.a['href']).build(csvfile)
                print('page written')
                    #time.sleep(5)
webScraper()
