            
import requests
from bs4 import BeautifulSoup

def get_post_comments(url):
    post_comments = []
    response = requests.get(url)

    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all(class_="comment")

    for item in content[1:]:
        comments = item.find_all(class_="usertext-body")
        for comment in comments:
            text = comment.get_text(strip=True)  
            post_comments.append(text)  
    return post_comments 