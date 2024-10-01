import os
import requests
import base64
from openai import AzureOpenAI# Configuration
endpoint = os.getenv("ENDPOINT_URL", "https://midh2.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "d4c8f79efc774d6d88f952a2111d77bd")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint = endpoint,
    api_key = subscription_key,
    api_version = "2024-05-01-preview",
)
class GPTInference:
    def get_from_markdown(file_path):  
        with open(file_path, 'r') as file:  
            abc = file.read()  
        return abc 
     
        

    def inference(self,prompt,temperature=0.7, top_p=0.95, max_tokens=800):
        # Payload for the request
        try:  
            payload = {  
                "model": deployment,  
                "messages": [  
                    {  
                        "role": "system",  
                        "content": "You are an AI assistant that helps people find information."  
                    },  
                    {  
                        "role": "user",  
                        "content": prompt  
                    }  
                ],  
                "temperature": temperature,  
                "top_p": top_p,  
                "max_tokens": max_tokens  
            }  
        
            response = client.chat.completions.create(**payload) 
            return response.to_dict() 
        
            # Do something with the response  
            
        
        except Exception as e:  
            # Handle the exception  
            print("An error occurred:", e)  
        
if __name__ == "__main__":
    # Initialize the GPTInference class
    pmpt=GPTInference()
    text="this is a paragraph i want you to to provide the response in this form field:value here , what im providing is a textual representation of the back of a product label.The fields that i require are as follows-1)date 2)nutrional information 3)ingredients 4)quantity its necessary that you dont hallucinate and dont fill in information that dosent exist return none"
    text+=GPTInference.get_from_markdown("/home/muhd/Desktop/GRID/src/ocr/output.md")

    response=pmpt.inference(text)
    
    print("*************************************")
    print(response.ChatCompletion[0].choices.message.content)