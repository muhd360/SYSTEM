import fal_client
import json
import logging
import base64
import os

class VisionLanguageModel:
    def describe_image(self, image_path_or_url):
        try:
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
                    "prompt": "You are an awesome product observer. Respond in JSON and get the following things about this item: expiry date, category it belongs to, name, mrp",
                    "system_prompt": "Provide a concise but detailed description of the product image.",
                    "image_url": image_url,
                },
                with_logs=False,
            )
            
            # Assuming the result is a dictionary with a 'response' key containing the JSON string
            if isinstance(result, dict) and 'response' in result:
                json_str = result['response']
                # Parse the JSON string into a Python dictionary
                parsed_result = json.loads(json_str)
                return parsed_result
            else:
                logging.error(f"Unexpected result format: {result}")
                return {}
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON response: {e}")
            return {}
        except Exception as e:
            logging.error(f"Error in describe_image: {e}")
            return {}
