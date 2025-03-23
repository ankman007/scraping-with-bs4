import json
from datetime import datetime
import os 

def get_relevant_posts(search_queries):
    folder_name = "data"
    file_list = os.listdir(folder_name)
    matching_posts = []
    for file in file_list:
        folder_path = os.path.join(folder_name, file)
        with open(folder_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        children = data["data"]["children"]

        for child in children:
            post_data = child['data']

            title = post_data['title']
            permalink = post_data['url']
            author_username = post_data['author_fullname']
            post_description = post_data['selftext']
            post_id = post_data['id']
            num_comments = post_data['num_comments']

            date = datetime.fromtimestamp(post_data['created'])
            created_at = date.strftime("%b %d, %Y")
            
            found_match = False
            for query in search_queries:
                if query.lower() in title.lower() or query.lower() in post_description.lower():
                    found_match = True
                    break  

            if found_match:
                matching_posts.append({
                    "title": title,
                    "permalink": permalink,
                    "author_username": author_username,
                    "post_description": post_description,
                    "post_id": post_id,
                    "num_comments": num_comments,
                    "created_at": created_at
                })
                
        return matching_posts
    
def main():
    search_queries = [
        "GBP suspension",
        "Google My Business suspension",
        "GMB suspension",
        "Suspended GBP",
        "address verification issues",
        "invalid address Google My Business",
        "Google Business Profile reinstatement",
        "reinstating suspended GBP",
        "Google My Business appeal",
        "service area business suspension",
        "suspension",
        "gbp",
        "suspended",
        "appeal"
        "google support",
        "deceptive content",
        "Suspension Delays"
    ]
    posts = get_relevant_posts(search_queries)
    with open("data.json", "w", encoding="utf-8") as outfile:
        json.dump(posts, outfile, indent=4)

    print(f"{len(posts)} matching posts saved to matching_posts.json", )
    
if __name__ == "__main__":
    main()