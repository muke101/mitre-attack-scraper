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
            
pt3Removal = ['References', 'None']
def pt3Scraper():
    pt3Dict = {}
    for tag in soup.find_all(class_='pt-3'):
       strings = tag.string
       print(strings)


print(pt3Scraper())
