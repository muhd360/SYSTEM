# ocr_extractor.py
import fal_client
import re


class OCRExtractor:
    def __init__(self, api_key):
        self.api_key = api_key

    def process_image(self, image_url):
        """
        Submits the image URL to the FAL API for OCR and returns the result.
        """
        result = fal_client.subscribe(
            "fal-ai/any-llm/vision",
            arguments={
                "model": "google/gemini-flash-1.5-8b",
                "prompt": "Caption this image for a text-to-image model with as much detail as possible.",
                "system_prompt": "Only answer the question, do not provide any additional information or add any prefix/suffix other than the answer of the original question. Don't use markdown.",
                "image_url": "https://fal.media/files/tiger/4Ew1xYW6oZCs6STQVC7V8_86440216d0fe42e4b826d03a2121468e.jpg",
            },
            with_logs=False,
        )
        return result.output

    def parse_ocr_result(self, result):
        """
        Parses the OCR result to extract the relevant information.
        """
        extracted_data = {}

        # Example: Extract expiry date
        expiry_match = re.search(
            r"\b(Expiry|Expires|Best before)\b\s*:?\s*(\d{2}/\d{2}/\d{4})", result
        )
        extracted_data["expiry_date"] = (
            expiry_match.group(2) if expiry_match else "Not found"
        )

        # Example: Extract product category
        category_match = re.search(r"\b(Category|Product)\b\s*:?\s*(\w+)", result)
        extracted_data["product_category"] = (
            category_match.group(2) if category_match else "Unknown"
        )

        return extracted_data
