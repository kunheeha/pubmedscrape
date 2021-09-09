# https://pubmed.ncbi.nlm.nih.gov/?term=search+words
import requests
from bs4 import BeautifulSoup

keywords = input('Search: ')
results_file = open(f'{keywords}.txt', 'x')
results_file.close()
keyword_list = keywords.split()
search = ""
for i in range(len(keyword_list)-1):
    search += keyword_list[i]
    search += '+'
search += keyword_list[-1]

source = requests.get(f'https://pubmed.ncbi.nlm.nih.gov/?term={search}').text
soup = BeautifulSoup(source, 'lxml')
articles = soup.find_all('article', class_='full-docsum')
article_links=[]
for article in articles:
    article_links.append(article.a.get('href'))

def article_details(link):
    source = requests.get(f'https://pubmed.ncbi.nlm.nih.gov/{link}').text
    soup = BeautifulSoup(source, 'lxml')
    title = soup.find('h1', class_='heading-title').get_text().strip()
    full_texts_list = []
    full_text_links = soup.find('div', class_='full-text-links-list')
    for link in full_text_links.find_all('a'):
        full_texts_list.append(link.get('href'))
    try:
        abstract_div = soup.find('div', class_='abstract-content')
        abstract = abstract_div.p.get_text()
        abstract.replace('\n', '')
    except:
        abstract = "No abstract"

    details = f'''
    Title: 

        {title}

    Abstract: {abstract}
    Full Text Links: {full_texts_list}

    -----------------

    '''

    return details 

results_file = open(f'{keywords}.txt', 'a')
for link in article_links:
    results_file.write(article_details(link))

results_file.close()

print(f'Finished, results stored in {keywords}.txt')


