import time
import requests
from bs4 import BeautifulSoup
from reddit.constants import HEADERS, URL


def fetch_reddit_posts(subreddit, pages=2):
    all_posts = []
    pagination_token = None
    for _ in range(pages):
        url = f"{URL}{subreddit}.json"
        if pagination_token:
            url += f"?after={pagination_token}"
            
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error {response.status_code} for {url}")
            break  
        
        content = response.json()
        posts = content["data"]["children"]
        for post in posts:
            post["data"]["subreddit"] = subreddit
            all_posts.append(post["data"])
        
        pagination_token = content["data"]["after"]
        if not pagination_token:
            break 
        time.sleep(3)
    
    return all_posts


def fetch_comments_from_posts(url):
    response = requests.get(url, headers=HEADERS)

    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all(class_="comment")
    
    post_comments = []
    for item in content[1:]:
        comments = item.find_all(class_="usertext-body")
        for comment in comments:
            text = comment.get_text(strip=True)  
            post_comments.append(text)  
            
    return post_comments

