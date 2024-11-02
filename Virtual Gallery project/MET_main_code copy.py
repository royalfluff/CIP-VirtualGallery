import json
import requests
from PIL import Image
from io import BytesIO
from urllib.request import urlopen
from urllib.parse import quote

API_SEARCH_BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/search?"
API_OBJECT_BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
SEARCH_TERM= "person"
SEARCH_LIMIT = 5


def search_objects(search_term):
    params= {
        "q":search_term,
        "hasImages":True, 
        "isHighlight":True
    }
    
    response = requests.get(API_SEARCH_BASE_URL, params=params)
    results = response.json()

    limited_results = results.get("objectIDs", [])[:SEARCH_LIMIT]
    return {"objectIDs": limited_results}

def display_results(search_results):
    im_ids = search_results.get("objectIDs",[])

    for im_id in im_ids:

        object_data = requests.get(API_OBJECT_BASE_URL+str(im_id))

        object_data= object_data.json()

        im_url= object_data.get('primaryImageSmall', None)
        im_url = quote(im_url, safe=':/')

        print(im_url)
        
        # Open the image with Pillow
        im = Image.open(urlopen(im_url))
        im.show()




search_term=SEARCH_TERM
search_results = search_objects(search_term)
display_results(search_results)
print("")

