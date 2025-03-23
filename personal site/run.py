import requests 
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def scrape_sitemap(base_url):
    response = requests.get(base_url, headers=headers)
    xml_data = response.content 
    soup = BeautifulSoup(xml_data, "xml")
    posts = soup.find_all("url")
    post_urls = []

    for post in posts:
        post_urls.append(post.select("loc")[0].text.strip())
    
    return post_urls
    
def main():
    url = "https://www.ankit-poudel.com.np/sitemap.xml"
    scrape_sitemap(url)
    
if __name__ == "__main__":
    # main()
    pass 

def get_blog_details():
    pass 

url = "https://www.ankit-poudel.com.np/2023/10/rest-api.html"
response = requests.get(url, headers=headers)
html = response.content
soup = BeautifulSoup(html, "html.parser")

article = soup.find(class_="blog-posts")
post_title = article.select('h1')[0].text.strip()
thumbnail = article.select('.post-body')[0].select('.separator')[0].find('a')['href']
print(article)