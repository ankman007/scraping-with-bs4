import os 
import requests 
from bs4 import BeautifulSoup 
import pandas as pd
import csv

base_url = "https://quotes.toscrape.com"
folder_name = 'data'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

def scrape_quotes():
    page_number = 1
    url = base_url + f"/page/{page_number}"
    file_name = 'quotes.csv'
    file_path = os.path.join(folder_name, file_name)

    with open(file_path, 'a+', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['quote', 'author', 'author_bio_url', 'tags'])
        
        while True: 
            response = requests.get(url)
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            quotes = soup.select('.container')[0].find_all(class_='quote')
                
            for quote in quotes:
                text = quote.select('.text')[0].text.strip()
                author = quote.find_all(class_='author')[0].text.strip()
                author_bio_url = base_url + quote.find_all('a')[0]['href']
                tags = quote.select('.tags')[0].select('.keywords')[0]['content']
                print(f'Quote: {text}\nAuthor: {author}\nAuthor Bio URL: {author_bio_url}\nTags: {tags}\n\n')
                writer.writerow([text, author, author_bio_url, tags])
                
            try: 
                next_page_url = soup.select_one('nav .next a')
                url = base_url + next_page_url['href']
                
            except: 
                break
        
def scrape_quote_by_tags():
    response = requests.get(base_url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    tags = soup.select('.container')[0].find_all(class_='tag-item')
    for tag in tags:
        tag_name = tag.select('a')[0].text.strip()
        tag_url = base_url + tag.select('a')[0]['href']
        print(f"{tag_name}: {tag_url}")
        
    
scrape_quote_by_tags()