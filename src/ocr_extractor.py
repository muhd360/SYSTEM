import fal_client
import re

class OCRExtractor:
    def __init__(self, api_key):
        self.api_key = api_key

    def process_image(self, image_url):
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

    def parse_ocr_result(self, result):
        extracted_data = {}

        # Extract expiry date
        expiry_match = re.search(r"\b(Expiry|Expires|Best before)\b\s*:?\s*(\d{2}/\d{2}/\d{4})", result)
        extracted_data["expiry_date"] = expiry_match.group(2) if expiry_match else "Not found"

        # Extract product category
        category_match = re.search(r"\b(Category|Product)\b\s*:?\s*(\w+)", result)
        extracted_data["product_category"] = category_match.group(2) if category_match else "Unknown"

        # Extract product name
        name_match = re.search(r"\b(Product|Item)\b\s*:?\s*(\w+(\s+\w+)*)", result)
        extracted_data["product_name"] = name_match.group(2) if name_match else "Unknown"

        # Extract MRP
        mrp_match = re.search(r"\b(MRP|Price)\b\s*:?\s*(\d+(\.\d{2})?)", result)
        extracted_data["mrp"] = mrp_match.group(2) if mrp_match else "Not found"

        return extracted_data
