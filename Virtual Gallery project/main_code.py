import requests
from PIL import Image
from io import BytesIO
import time
from urllib.request import urlopen

API_KEY = "11505413-2a12-48e2-8123-3743409c7c4d"
API_BASE_URL = " https://api.harvardartmuseums.org/object?"
MIRADOR_URL = "https://iiif.harvardartmuseums.org/viewers/mirador/v2"


def search_objects(search_term):
    params= {
        "keyword":search_term,
        "apikey": API_KEY,  
        "hasimage":1,
        "century": "18th century"
    }
    
    response = requests.get(API_BASE_URL, params=params)
    return response.json()

def display_results(search_results):
    objects = search_results.get("records", [])
    for object in objects:
        if "images" in object and object["images"]:
            # Construct IIIF URL from iiifbaseuri for a direct image link
            iiif_url = f"{object['images'][0]['iiifbaseuri']}/full/full/0/default.jpg"
            print("Image URL:", iiif_url)
            
            # Fetch image data from URL with User-Agent header
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
            }

            # Retry fetching the image if it is still processing
            max_retries = 3
            for attempt in range(max_retries):
                #time.sleep(5)  # Allow time for processing

                # Fetch image data from URL
                image_response = requests.get(iiif_url, headers=headers)
                #print("Image Status Code:", image_response.status_code)

                if image_response.status_code:
                    try:
                        
                        # Open the image with Pillow
                        # im = Image.open(urlopen(iiif_url))
                        im = Image.open(requests.get(iiif_url, stream=True).raw)

                        #im = Image.open(BytesIO(image_response.content))
                        print(f"Image Format: {im.format}, Size: {im.size}, Mode: {im.mode}")
                        break  # Exit loop on success
                    
                    except Exception as e:
                        print(f"Failed to open image with Pillow: {e}")
                        break  # Exit on error
                
                elif image_response.status_code == 202:
                    print("Image is still processing, retrying...")
                    #time.sleep(5)
                
                else:
                    print(f"Failed to retrieve image: {iiif_url}, Status Code: {image_response.status_code}")
                    break  # Exit loop on other failures
        
        else:
            print("No images found for this object.")


while True:
    search_term=input("Your search term: ")
    search_results = search_objects(search_term)
    display_results(search_results)
    print("")

