import os 
from bs4 import BeautifulSoup
import csv 
import requests

folder_path = "data"
file_name = "books.csv"
page_number = 1
url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

file_path = os.path.join(folder_path, file_name)

while True:

    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")
    ol = soup.select('ol')[0]
    products = ol.find_all('li')
    
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        
        writer = csv.writer(file)
        writer.writerow(['Book Title', 'Image URL', 'Rating', 'Price', 'Availability'])

        for product in products:
            book_title = product.find('h3').find('a')["title"]
            image_url = "http:" + product.find('img')["src"]
            rating = product.find('p')["class"][1]
            price = product.select('.product_price')[0].find('p').text.strip()
            is_available = product.select('.product_price')[0].find_all('p')[1].text.strip()
            
            print(f"Title: {book_title} | Image URL: {image_url} | Rating: {rating} | Price: {price} | Availability: {is_available}")
            
            writer.writerow([book_title, image_url, rating, price, is_available])
            
    try:
        next_page_link = soup.find('li', class_='next').find('a')['href']
        page_number += 1
        url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
    
    except AttributeError: 
        break
        
        
