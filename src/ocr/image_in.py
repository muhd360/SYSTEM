import io
import requests
import json
import os
from PIL import Image   
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Metadata:
    width: int
    height: int

@dataclass
class BoundingPolygon:
    x: int
    y: int

@dataclass
class Word:
    text: str
    boundingPolygon: List[BoundingPolygon]
    confidence: float  

@dataclass
class Line:
    text: str
    boundingPolygon: List[BoundingPolygon]
    words: List[Word]    

@dataclass
class Block:
    lines: List[Line]

@dataclass
class ReadResult:
    blocks: List[Block]

@dataclass
class AnalyzeResult:
    modelVersion: str
    metadata: Metadata
    readResult: ReadResult

@dataclass
class AnalyzeRequest:
    uri: str

class OCR:
    def recognize_text(self):
        # For prod environment, please find the endpoint and resource key of your computer vision resource from Azure portal.
        endpoint = "https://ai-amirzakaria123456789ai439277757577.openai.azure.com/"
        url = f"{endpoint}computervision/imageanalysis:analyze?features=read&gender-neutral-caption=false&api-version=2023-10-01"
        key = "968b626644114e568958de19620bbd74"

        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Content-Type': 'application/json; charset=utf-8'
        }

        # with image url
        image_url = "https://ai.azure.com/common/vision/extractText/extract-text-sample-5.jpg"
        image_path="/home/muhd/Desktop/GRID/images/Produce/label.jpeg"
        file_size = os.path.getsize(image_path)
        print(f"Image size: {file_size / 1024} KB")
        with Image.open(image_path) as img:
            img = img.resize((800, 600)) 
            print(img.size) # Resize the image (you can adjust the dimensions)
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG')
            image_data = buffer.getvalue()

        #response = requests.post(url, headers=headers, json=analyze_request)
        response = requests.post(url, headers=headers, data=image_data)
       


        # Print the JSON response for debugging
        #print("Response Content:", response_content)
        answer=""

        # Deserialize and print the result
        data = response.json()
        print(data)
        try:
            deserialized_object = self.from_dict(AnalyzeResult, data)

            #print(f"Model Version: {deserialized_object.modelVersion}")
            #print(f"Metadata - Width: {deserialized_object.metadata.width}, Height: {deserialized_object.metadata.height}")
            for block in deserialized_object.readResult.blocks:
                for line in block.lines:
                    answer+=line.text

            print(answer)
            return answer               
   
        except KeyError as e:
            print(f"KeyError: {e}. Please check the JSON response structure.")

            return None

    def from_dict(self, data_class, data):
        if isinstance(data, list):
            return [self.from_dict(data_class.__args__[0], item) for item in data]
        if isinstance(data, dict):
            fieldtypes = {f.name: f.type for f in data_class.__dataclass_fields__.values()}
            return data_class(**{k: self.from_dict(fieldtypes[k], v) for k, v in data.items()})
        return data
    def to_markdown(self,x, filename):
        try:
            # Open the file in write mode (will create or overwrite the file)
            with open(filename, "w") as file:
                # Write the response (assumed to be a string) to the markdown file
                file.write(str(x))

            print(f"Markdown file '{filename}' created successfully.")

        except Exception as e:
            print(f"An error occurred while writing to the markdown file: {e}")


# Usage example
if __name__ == "__main__":
    ocr = OCR()
    
    
    ocr.to_markdown(ocr.recognize_text(),"output.md")
