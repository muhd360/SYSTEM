import pytesseract
from PIL import Image

class TextDetector:
    def detect_text(self, image_path_or_url):
        img = load_image(image_path_or_url)
        text = pytesseract.image_to_string(img)
        return text
