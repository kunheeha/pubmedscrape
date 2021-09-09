# Scraping from PubMed - database of biomedical literature
# https://pubmed.ncbi.nlm.nih.gov/?term=example+search+words
import requests
from bs4 import BeautifulSoup

# Take User Input of Search keywords
keywords = input('Search: ')
# Create txt file named after search keywords
results_file = open(f'{keywords}.txt', 'x')
results_file.close()
# formatting search keywords to 'exmaple+search+words' 
keyword_list = keywords.split()
search = ""
for i in range(len(keyword_list)-1):
    search += keyword_list[i]
    search += '+'
search += keyword_list[-1]

# Scraping all links to first 10 articles
source = requests.get(f'https://pubmed.ncbi.nlm.nih.gov/?term={search}').text
soup = BeautifulSoup(source, 'lxml')
articles = soup.find_all('article', class_='full-docsum')
article_links=[]
for article in articles:
    article_links.append(article.a.get('href'))

# Scraping title, abstract, links to full text from links above
def article_details(link):
    source = requests.get(f'https://pubmed.ncbi.nlm.nih.gov/{link}').text
    soup = BeautifulSoup(source, 'lxml')
    title = soup.find('h1', class_='heading-title').get_text().strip()
    full_texts_list = []
    full_text_links = soup.find('div', class_='full-text-links-list')
    for link in full_text_links.find_all('a'):
        full_texts_list.append(link.get('href'))
    # Try Except because some may not have an abstract
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

# Store results in txt file created at start
results_file = open(f'{keywords}.txt', 'a')
for link in article_links:
    results_file.write(article_details(link))

results_file.close()

print(f'Finished, results stored in {keywords}.txt')


