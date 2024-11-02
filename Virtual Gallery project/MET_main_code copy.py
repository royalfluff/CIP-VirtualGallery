import json
import requests
from PIL import Image, ImageTk
from io import BytesIO
from urllib.request import urlopen
from urllib.parse import quote
import tkinter as tk

API_SEARCH_BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/search?"
API_OBJECT_BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"

SEARCH_TERM= "person"
SEARCH_LIMIT = 1

MAX_WIDTH = 400
MAX_HEIGHT = 400


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

def find_url(search_results):
    im_ids = search_results.get("objectIDs",[])

    for im_id in im_ids:

        object_data = requests.get(API_OBJECT_BASE_URL+str(im_id))

        object_data= object_data.json()

        im_url= object_data.get('primaryImageSmall', None)
        im_url = quote(im_url, safe=':/')

        print(im_url)
        
        return im_url

def load_im(im_url):
    # Open the image with Pillow
    im = Image.open(urlopen(im_url))
    return im 
    
def resize_image(im, max_width, max_height):
 
    #Resize the image while maintaining aspect ratio.
    original_width, original_height = im.size
    aspect_ratio = original_width / original_height

    if original_width > max_width or original_height > max_height:
        if aspect_ratio > 1:  # Wider than tall
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:  # Taller than wide
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
    else:
        return im  # Return original if it fits

    return im.resize((new_width, new_height), Image.LANCZOS)


def set_up_tk(pil_im):
    # Initialize the main window
    root = tk.Tk()
    root.title("Art Gallery")
    root.geometry("600x800")  # Set the window size

    # Create a label to hold the image
    image_label = tk.Label(root)
    image_label.pack()

    if pil_im:
        resized_im = resize_image(pil_im, MAX_WIDTH, MAX_HEIGHT)  # Resize while maintaining aspect ratio
        tk_im = ImageTk.PhotoImage(resized_im)
        
        # Update the image label to display the new image
        image_label.configure(image=tk_im)
        image_label.image = tk_im  # Keep a reference to avoid garbage collection

    root.mainloop()  # Start the Tkinter event loop



    

search_results = search_objects(SEARCH_TERM)  # Finds all objects and limits results
im_url = find_url(search_results)  # Locates object ID from result data
if im_url:
    pil_im = load_im(im_url)  # Loads image using Pillow
    set_up_tk(pil_im)  # Set up Tkinter window with the image
else:
    print("No image URL found.")

print("")

