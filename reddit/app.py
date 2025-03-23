import requests
import os
import json 

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

def main():
    base_url = "https://old.reddit.com/r/"
    subreddits = ["googlemybusiness", "localseo"]    
    save_reddit_json_data(base_url, subreddits)
    
if __name__ == "__main__":
    # main()
    pass