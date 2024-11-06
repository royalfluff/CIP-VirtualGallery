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
SEARCH_LIMIT = 15

#for images -
MAX_WIDTH = 800
MAX_HEIGHT = 800


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

# Function to find image URLs
def find_url(search_results):
    im_ids = search_results.get("objectIDs",[])

    url_list = []

    for im_id in im_ids:

        object_data = requests.get(API_OBJECT_BASE_URL+str(im_id))

        object_data= object_data.json()

        im_url= object_data.get('primaryImageSmall', None)
        im_url = quote(im_url, safe=':/')

        #print(im_url)
        url_list.append(im_url)

    return url_list

def load_im(im_url):    
    # load the image with Pillow
    im = Image.open(urlopen(im_url))
    return im 
    
def resize_image(im, max_width, max_height):

    """
    Resizes an image while maintaining its aspect ratio, then pastes it onto
    a blank background of specified dimensions to ensure consistent display size.
    """
 
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

    resized_im =  im.resize((new_width, new_height), Image.LANCZOS)

    #create a blank, black background
    background = Image.new("RGB", (max_width, max_height), "black")

    #center and paste the resized images onto the bg
    x_offset= (max_width-new_width)//2
    y_offset= (max_height-new_height)//2
    background.paste(resized_im,(x_offset,y_offset))

    return background


def update_image(image_label,url_list, current_index):
    url = url_list[current_index[0]]
    pil_img = load_im(url)

    if pil_img:
        resized_im = resize_image(pil_img, MAX_WIDTH, MAX_HEIGHT)  # Resize while maintaining aspect ratio
        tk_im = ImageTk.PhotoImage(resized_im)
        
        # Update the image label to display the new image
        image_label.configure(image=tk_im)
        image_label.image = tk_im  # Keep a reference to avoid garbage collection


def set_up_tk(url_list):
    # Initialize the main window
    root = tk.Tk()
    root.title("Art Gallery")
    root.geometry("1080x900")  # Set the window size
    

    #frame to hold the image
    frame= tk.Frame(root, bd=5, relief = tk.SUNKEN)
    frame.pack(pady=20)

    # Create a label to hold the image
    image_label = tk.Label(frame)
    image_label.pack()

    current_index = [0]  # Mutable list to track current index


    def next_image(event=None): #Accept an event parameter for keyboard binding
        current_index[0]= (current_index[0]+1)% len(url_list)
        update_image(image_label,url_list, current_index)

    def prev_image(event=None): #Accept an event parameter for keyboard binding
        current_index[0]= (current_index[0]-1)% len(url_list)
        update_image(image_label,url_list, current_index)

    update_image(image_label,url_list, current_index)

    # Create a new frame for navigation buttons
    nav_frame = tk.Frame(root)
    nav_frame.pack(side="bottom",pady=20)

    #next controls
    next_button = tk.Button(nav_frame, text ="Next Artwork", command = next_image)
    next_button.pack(side=tk.RIGHT, padx=10)
    root.bind("<Right>", next_image)

    #prev controls
    prev_button= tk.Button(nav_frame, text = "Previous Artwork", command = prev_image)
    prev_button.pack(side=tk.LEFT,padx=10)
    root.bind("<Left>", prev_image)

    root.mainloop()  # Start the Tkinter event loop

    
def main():
    search_results = search_objects(SEARCH_TERM)  # Finds all objects and limits results
    url_list = find_url(search_results)  # Locates object ID from result data

    if url_list:
        #pil_im = load_im(im_url)  # Loads image using Pillow
        set_up_tk(url_list)  # Set up Tkinter window with the image
    else:
        print("No image URL found.")

    print("")

if __name__ == '__main__':
    main()

