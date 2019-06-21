from bs4 import BeautifulSoup
import re

page = open('T1028','rb')
#insert requesting here
soup = BeautifulSoup(page, 'html.parser')       
classes = ['card', 'col-md4 description-body']


cardRemoval = ['Version']
def cardScraper():
    cardDict = {}
    for tag in soup.find_all(class_='card-data'):
        strings = tag.strings
        key = next(strings) #TODO: stirp off random hex's
        if key != ' ': 
            cardDict[key] = [i for i in strings][0].strip(' :') 
    for entry in cardRemoval:
        del cardDict[entry]
    return cardDict
            
pt3Removal = ['references']
def pt3Scraper():
    pt3Dict = {}
    for tag in soup.find_all(class_='pt-3'):
        if tag['id'] not in pt3Removal:
            print(tag.next_sibling)
            break
print(soup.prettify())
#print(pt3Scraper())
