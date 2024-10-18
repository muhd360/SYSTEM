import fal_client
import re
import base64
import os

class OCRExtractor:
    def __init__(self, api_key):
        self.api_key = api_key

    def process_image(self, image_path_or_url):
        if image_path_or_url.startswith(('http://', 'https://')):
            image_url = image_path_or_url
        else:
            # If it's a local file, we need to encode it to base64
            with open(image_path_or_url, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{encoded_string}"

        result = fal_client.subscribe(
            "fal-ai/any-llm/vision",
            arguments={
                "model": "google/gemini-flash-1.5-8b",
                "prompt": "Extract all text visible in this image, including product details, expiry dates, and prices.",
                "system_prompt": "Extract text accurately without additional commentary.",
                "image_url": image_url,
            },
            with_logs=False,
        )
        return result.output

