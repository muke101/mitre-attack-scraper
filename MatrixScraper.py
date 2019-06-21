from bs4 import BeautifulSoup
import re

page = open('T1028','rb')

classes = ['card', 'col-md4 description-body']


def pageScraper(url):
    #insert requesting here
    soup = BeautifulSoup(url, 'html.parser')       
    for className in classes:
        for tag in soup.find_all(class_='card-data'):
                print([i.get_text() for i in tag.children])
#    for tag in soup.find_all(class_='pt-3'): #this class in unique so iterating seperately in a less 'modular' way
            
pageScraper(page)
