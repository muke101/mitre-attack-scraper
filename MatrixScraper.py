from bs4 import BeautifulSoup
import requests
import time
import re

class pageScraper:
    def __init__(self, page):
        page = requests.get(page)
        self.soup = BeautifulSoup(page.text, 'html.parser')       
        self.cardRemoval = ['Version']
        self.pt3Removal = ['references', 'examples'] 
    
    def cardScraper(self):
        cardDict = {}
        for tag in self.soup.find_all(class_='card-data'):
            strings = tag.strings
            key = next(strings) #TODO: stirp off random hex's
            if key != ' ': 
                cardDict[key] = [i for i in strings][0].strip(' :') 
        for entry in self.cardRemoval:
            del cardDict[entry]
        return cardDict
                
    def pt3Scraper(self):
        pt3Dict = {}
        for tag in self.soup.find_all(class_='pt-3'):
            if tag['id'] not in self.pt3Removal:
                pt3Dict[tag.contents[0]] = tag.next_sibling.next_sibling.contents[0] 
        return pt3Dict
    
    def descBodyScraper(self):
        descs = []
        for tag in self.soup.find(class_='col-md-8 description-body').contents:
            if tag != '\n':
                descs.append(tag.get_text())
        return descs
    
    def build(self):
        resultDict = {}
        resultDict['card'] = self.cardScraper()
        resultDict['pt3'] = self.pt3Scraper()
        resultDict['descBody'] = self.descBodyScraper()
        return resultDict


def webScraper():
    soup = BeautifulSoup(open('windows','rb'), 'html.parser')       
    for row in soup.tbody.children:
        if row != '\n':
            for box in row:
                if box != '\n' and box.a != None:
                    yield pageScraper('https://attack.mitre.org'+box.a['href']).build()

for scrape in webScraper():
    print(scrape)
    time.sleep(10)
