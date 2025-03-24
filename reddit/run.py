import json
import os 
import requests
from reddit.utils import get_post_comments
from reddit.constant import search_queries, subreddits


def scrape(folder_name=None):
    base_url = "https://old.reddit.com/r/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    if folder_name is None:
        folder_name = os.path.join(os.path.dirname(__file__), "data")

    os.makedirs(folder_name, exist_ok=True)

    for subreddit in subreddits:
        url = base_url + subreddit + ".json"
        response = requests.get(url, headers=headers)

        file_name = f"{subreddit}.json"
        file_path = os.path.join(folder_name, file_name)

        content = response.json()
        with open(file_path, "w", encoding="utf-8", newline="") as file:
            json.dump(content, file, indent=4)
        print(f"Saved: {file_path}")


def analyze(search_queries):
    folder_name = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(folder_name):
        print(f"Error: Data folder '{folder_name}' does not exist. Run scrape() first.")
        return

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
                
    output_file = os.path.join(os.path.dirname(__file__), "data/relevant_posts.json")            
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(matching_posts, outfile, indent=4)

    print(f"{len(matching_posts)} matching posts saved to matching_posts.json", )
    
if __name__ == "__main__":
    # scrape()
    analyze(search_queries)
    pass 