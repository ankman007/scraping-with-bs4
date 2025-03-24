import json
import os 
import time
import requests
from bs4 import BeautifulSoup
from reddit.constant import search_queries, subreddits


def scrape_posts(folder_name=None, pages=3, subreddits=["localseo"]):
    base_url = "https://old.reddit.com/r/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    if folder_name is None:
        folder_name = os.path.join(os.path.dirname(__file__), "data")

    os.makedirs(folder_name, exist_ok=True)
    all_posts = []

    for subreddit in subreddits:
        pagination_token = None
        for _ in range(pages):
            url = f"{base_url}{subreddit}.json"
            if pagination_token:
                url += f"?after={pagination_token}"
                
            response = requests.get(url, headers=headers)
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
            
    file_path = os.path.join(folder_name, "posts.json")
    with open(file_path, "w", encoding="utf-8", newline="") as file:
        json.dump(all_posts, file, indent=4)
    print(f"Saved: {file_path}")


# def scrape_comments(url):
#     post_comments = []
#     response = requests.get(url)

#     html = response.content

#     soup = BeautifulSoup(html, 'html.parser')
#     content = soup.find_all(class_="comment")

#     for item in content[1:]:
#         comments = item.find_all(class_="usertext-body")
#         for comment in comments:
#             text = comment.get_text(strip=True)  
#             post_comments.append(text)  
#     return post_comments 


def analyze(search_queries):
    folder_name = os.path.join(os.path.dirname(__file__), "data")
    file_path = os.path.join(folder_name, "posts.json")

    matching_posts = []
    formatted_search_queries = [query.lower() for query in search_queries]  
    
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        

    for post_data in data:
        title = post_data['title']
        post_description = post_data.get("selftext", "")
        permalink = "https://www.reddit.com" + post_data.get("permalink", "")

        if any(query in title.lower() or query in post_description.lower() for query in formatted_search_queries):
            post_data["full_permalink"] = permalink  
            matching_posts.append(post_data)
                
    output_file = os.path.join(os.path.dirname(__file__), "data/output.json")            
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(matching_posts, outfile, indent=4)

    print(f"{len(matching_posts)} matching posts saved to output.json")
    
    
if __name__ == "__main__":
    scrape_posts(subreddits=subreddits)
    # scrape_comments()
    analyze(search_queries)
    pass 