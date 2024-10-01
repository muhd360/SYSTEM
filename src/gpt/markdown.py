import json  
  
class MarkdownToJsonConverter:  
    def __init__(self, markdown_text):  
        self.markdown_text = markdown_text  
  
    def convert(self):  
        # Split the markdown text into lines  
        lines = self.markdown_text.strip().split('\n')  
          
        # Dictionary to hold the JSON data  
        json_data = {}  
          
        # Process each line  
        for line in lines:  
            # Assuming each line is in the format "Key: Value"  
            if ": " in line:  
                key, value = line.split(": ", 1)  
                json_data[key.strip()] = value.strip()  
          
        return json_data  
  
# Example Markdown  
markdown_text = """  
Title: Sample Document  
Author: John Doe  
Date: 2021-09-01  
"""  
  
# Create an instance of the converter  
converter = MarkdownToJsonConverter(markdown_text)  
  
# Convert Markdown to JSON  
json_data = converter.convert()  
  
# Print the JSON output  
print(json.dumps(json_data, indent=4))  
