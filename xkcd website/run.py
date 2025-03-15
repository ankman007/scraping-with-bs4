import requests
from bs4 import BeautifulSoup
import os

base_url = "https://xkcd.com/"
folder_path = "images"
page_number = 3061

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

while True:
    try:
        print(f"Image number: {page_number}")
        
        # Request the webpage
        url = os.path.join(base_url, str(page_number))
        request = requests.get(url)

        # Parse the html content so we can use it 
        html_content = request.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the url of the image
        image_element = soup.select('#comic img')[0]
        image_src = "http:" + str(image_element["src"])
        image_name = os.path.basename(image_src)

        # Download the image
        response = requests.get(image_src)
        image_path = os.path.join(folder_path, image_name)
        
        if response.status_code == 200:
            with open(image_path, "wb") as file:
                file.write(response.content)
                print(f"Image saved: {image_name}")
        else:
            print(f"Error saving image: {image_name}")
        
        # Get the page number from next button for next iteration of the loop
        next_button = soup.select(".comicNav li a[rel='next']")[0]
        page_number = next_button['href'].strip('/')
        
        if page_number == "#":
            print("No more pages to fetch. Exiting.")
            break
        
    except Exception as e:
        print(f"Encountered error when fetching page {page_number}: {e}")
        continue
    
    
