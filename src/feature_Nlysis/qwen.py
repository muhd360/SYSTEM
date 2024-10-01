# Use a pipeline as a high-level helper
import torchvision
import transformers
import torch
import requests
import os
import json
import base64
from io import BytesIO
from transformers import pipeline
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor,CLIPImageProcessor
from qwen_vl_utils import process_vision_info
from PIL import Image
from huggingface_hub import InferenceClient



# API_ENDPOINT = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct"
# TOKEN='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'
# client = InferenceClient(
#     "Qwen/Qwen2.5-72B-Instruct",
#     token=TOKEN,
# )


# default processer
processor = CLIPImageProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct")
class A:
    def get_last_image(image_folder):
        # Get all files in the folder and filter only image files (e.g., .jpg, .png)
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

        if not image_files:
            raise ValueError(f"No images found in folder: {image_folder}")

        # Get the full path of each image and sort them by last modification time
        image_files = [os.path.join(image_folder, f) for f in image_files]
        image_files.sort(key=os.path.getmtime)  # Sort by modification time

        # Return the last (most recent) image
        
        return image_files[-1]


    def pil_image_to_base64(image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")  # You can change the format if needed
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_str

    def query_last_image(prompt, image_folder):
        """
        Query the model with the prompt and the last image in the folder via the API.
        """
        # Get the most recent image
        last_image = get_last_image(image_folder)
        last_image = Image.open(last_image)

        
        # Create message structure for the API request
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": pil_image_to_base64(last_image),  # Pass the most recent image
                    },
                    {"type": "text", "text": prompt},  # Include the text prompt
                ],
            }
        ]

        # Prepare the input using the processor and send it to the API
        inputs = processor(
            images=last_image,
            # messages=messages,
            # padding=True,
            return_tensors="pt"
        )
        try:
            response = requests.post(API_ENDPOINT,json=messages)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")
        #Inference via the API (model is not loaded locally, handled by the API)



        return response.json()

    def try1(self):
        model = Qwen2VLForConditionalGeneration.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
        processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": "What is shown in this image?"},
                ],
            },
        ]
        url = "https://www.ilankelman.org/stopsigns/australia.jpg"
        image = Image.open(requests.get(url, stream=True).raw)

        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = processor(text=[text], images=[image], vision_infos=[vision_infos])

        # Generate
        generate_ids = model.generate(inputs.input_ids, max_length=30)
        result=tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        return result

if __name__ == "__main__":
    a=A()
    a.try1()


