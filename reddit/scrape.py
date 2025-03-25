import json
import os 
import time
from reddit.constants import SUBREDDITS
from reddit.utils import fetch_reddit_posts, fetch_comments_from_posts
    
    
def scrape_posts(subreddits=SUBREDDITS):
    all_posts = []

    folder_name = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(folder_name, exist_ok=True)

    for subreddit in subreddits:
        all_posts.extend(fetch_reddit_posts(subreddit))
        all_posts.extend(fetch_reddit_posts(subreddit)) 

    file_path = os.path.join(folder_name, "posts.json")
    
    try: 
        with open(file_path, "w", encoding="utf-8", newline="") as file:
            json.dump(all_posts, file, indent=4)
        print(f"Saved: {file_path}")
    except IOError as e:
        print(f"Error saving posts.json: {e}")        
    

def scrape_comments():

    file_path = os.path.join(os.path.dirname(__file__), "data/posts.json")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            posts_data = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading posts.json: {e}")
        return
           
    for post in posts_data:
        url = "https://old.reddit.com" + post["permalink"]
        comments = fetch_comments_from_posts(url)
        post["comments"] = comments
        time.sleep(2)
        
    try: 
        with open(file_path, "w", encoding="utf-8", newline="") as file:
            json.dump(posts_data, file, indent=4)
        print(f"Saved: {file_path}")
    except IOError as e:
        print(f"Error saving posts.json: {e}")        
    
                
    
