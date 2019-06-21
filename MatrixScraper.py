from bs4 import BeautifilSoup

page = open('T1028','rb')
soup = BeautifulSoup(page, 'html.parser')

className = ['card', 'col-md4 description-body']

def pageScraper(url):
    soup = BeautifulSoup(url, 'html.parser')       
    for className in classes:
        for tag in soup.find(class_=className):
            
    for tag in soup.find_all(class_='pt-3'): #this class in unique so iterating seperately in a less 'modular' way
            

