import pytesseract
from PIL import Image
import requests
from io import BytesIO

class TextDetector:
    def detect_text(self, image_url):
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(img)
        return text

