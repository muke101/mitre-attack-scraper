from bs4 import BeautifulSoup
import requests
import time
import csv
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
                pt3Dict[tag.contents[0]] = re.sub('[\[\d\]]','',tag.next_sibling.next_sibling.contents[0]) 
        return pt3Dict
    
    def descBodyScraper(self): 
        descDict = {} 
        firstHeader = True
        for tag in self.soup.find(class_='col-md-8 description-body').contents:
            if tag != '\n':
                paragraphs = []
                if tag.name != 'h3':
                    paragraphs.append(re.sub('[\[\d\]]','',tag.get_text()))
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
    
    def build(self, csv, html):
        descDict = self.descBodyScraper()
        pt3Dict = self.pt3Scraper()
        cardDict = self.cardScraper()
        
        totalDict = {**descDict, **pt3Dict, **cardDict}
        csv.writerow([' '])
        for key in totalDict.keys():
            csv.writerow([self.pageName, key, totalDict[key]])
        csv.writerow('\n')

        html.write("<h1 id=\"title-text\" class=\"assistive\" style=\"display: block;\"><a>"+self.pageName+"</a> </h1><div><table><tbody><tr><td>Mitigation</td><td><p>"+pt3Dict['Mitigation']+"</p></td></tr><tr><td><p>Dectection</p></td><td><p>"+pt3Dict['Detection']+"</p></td></tr></tbody></table></div>")
        html.write("\n")
    


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
