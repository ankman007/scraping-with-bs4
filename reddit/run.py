import json
import os 
import requests
from bs4 import BeautifulSoup

def save_reddit_json_data(base_url, subreddits, folder_name="data"):
    os.makedirs(folder_name, exist_ok=True)
    headers = {'User-Agent': 'Mozilla/5.0'}

    for subreddit in subreddits:
        url = base_url + subreddit + ".json"
        response = requests.get(url, headers=headers)
        
        file_name = subreddit + ".json"
        file_path = os.path.join(folder_name, file_name)

        content = json.loads(response.content)
        with open(file_path, "w", encoding="utf-8", newline="") as file:
            json.dump(content, file, indent=4)
   
            
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


def find_matching_posts(search_queries):
    folder_name = "data"
    file_list = os.listdir(folder_name)
    matching_posts = []
    formatted_search_queries = [query.lower() for query in search_queries]  
    
    for file in file_list:
        folder_path = os.path.join(folder_name, file)
        with open(folder_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            
        children = data["data"]["children"]

        for child in children:
            post_data = child['data']
            title = post_data['title']
            post_description = post_data['selftext']
            permalink = post_data['url']

            if any(query in title.lower() or query in post_description.lower() for query in formatted_search_queries):
                matching_posts.append(child)
                continue  

            comments = get_post_comments(permalink)
            if any(query in comment.lower() for query in formatted_search_queries for comment in comments):
                matching_posts.append(child)
                
    return matching_posts
    
    
def main():
    base_url = "https://old.reddit.com/r/"
    subreddits = ["googlemybusiness", "localseo"]    
    save_reddit_json_data(base_url, subreddits)
    
    search_queries = [
        "GBP suspension",
        "Google My Business suspension",
        "GMB suspension",
        "Suspended GBP",
        "address verification issues",
        "invalid address Google My Business",
        "Google Business Profile reinstatement",
        "reinstating suspended GBP",
        "unsuspended",
        "reinstated",
        "disabled",
        "policy violations",
        "Google My Business appeal",
        "service area business suspension",
        "Profile Verifications",
        "suspension",
        "gbp",
        "suspended",
        "appeal",
        "google support",
        "deceptive content",
        "Suspension Delays",
    ]
    
    posts = find_matching_posts(search_queries)
    with open("data.json", "w", encoding="utf-8") as outfile:
        json.dump(posts, outfile, indent=4)

    print(f"{len(posts)} matching posts saved to matching_posts.json", )
    
    
if __name__ == "__main__":
    # main()
    pass 