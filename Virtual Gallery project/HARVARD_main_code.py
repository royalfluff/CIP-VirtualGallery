import requests
from PIL import Image
from io import BytesIO
import time
from urllib.request import urlopen

API_KEY = "11505413-2a12-48e2-8123-3743409c7c4d"
API_BASE_URL = " https://api.harvardartmuseums.org/object?"


def search_objects(search_term):
    params= {
        "keyword":search_term,
        "apikey": API_KEY,  
        "hasimage":1,
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
            
            # Open the image with Pillow
            im = Image.open(urlopen(iiif_url))

            break  # Exit loop on success

    else:
        print("No images found for this object.")


while True:
    search_term=input("Your search term: ")
    search_results = search_objects(search_term)
    display_results(search_results)
    print("")

