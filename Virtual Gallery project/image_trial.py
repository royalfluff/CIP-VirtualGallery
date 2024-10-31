from PIL import Image
import requests
from io import BytesIO

image_url = "https://images.metmuseum.org/CRDImages/as/web-large/DP251139.jpg"
response = requests.get(image_url)
if response.status_code == 200:
    img = Image.open(BytesIO(response.content)) 
    img.show()  # This should open in your default image viewer.
else:
    print("Failed to retrieve image.")