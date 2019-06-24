from bs4 import BeautifulSoup
import requests
import time
import csv
import re

class pageScraper:
    def __init__(self, page):
        page = requests.get(page)
        self.soup = BeautifulSoup(page.text, 'html.parser')       
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
                pt3Dict[tag.contents[0]] = tag.next_sibling.next_sibling.contents[0] 
        return pt3Dict
    
    def descBodyScraper(self): #TODO: remove referance tags
        descDict = {} 
        firstHeader = True
        for tag in self.soup.find(class_='col-md-8 description-body').contents:
            if tag != '\n':
                paragraphs = []
                if tag.name != 'h3':
                    paragraphs.append(tag.get_text())
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
    
    def build(self, csv):
        totalDict = {**self.descBodyScraper(), **self.pt3Scraper(), **self.cardScraper()}
        csv.writerow([' '])
        csv.writerow(['Page', self.pageName])
        for key in totalDict.keys():
            csv.writerow([key, totalDict[key]])

def webScraper():
    csvfile = csv.writer(open('output.csv', 'w'), delimiter=':')
    soup = BeautifulSoup(open('windows','rb'), 'html.parser')       
    for row in soup.tbody.children:
        if row != '\n':
            for box in row:
                if box != '\n' and box.a != None:
                    pageScraper('https://attack.mitre.org'+box.a['href']).build(csvfile)
                    print('page written')
                    time.sleep(5)

webScraper()
