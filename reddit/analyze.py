import os 
import json 
from reddit.constants import SEARCH_QUERIES


def filter_posts(search_queries=SEARCH_QUERIES):
    folder_name = os.path.join(os.path.dirname(__file__), "data")
    file_path = os.path.join(folder_name, "posts.json")

    matching_posts = []
    formatted_search_queries = [query.lower() for query in search_queries]  
    
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for post_data in data:
        title = post_data['title']
        post_description = post_data.get("selftext", "")
        comments = post_data.get("comments")
        permalink = "https://www.reddit.com" + post_data.get("permalink", "")

        if any(query in title.lower() or query in post_description.lower() for query in formatted_search_queries):
            post_data["full_permalink"] = permalink  
            matching_posts.append(post_data)
            continue
        
        for comment in comments:
            if any(query in comment.lower() for query in formatted_search_queries):
                post_data["full_permalink"] = permalink
                matching_posts.append(post_data)
                break 
                
    output_file = os.path.join(os.path.dirname(__file__), "data/output.json")            
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(matching_posts, outfile, indent=4)

    print(f"{len(matching_posts)} matching posts saved to output.json")
  