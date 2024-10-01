import os
from openai import AzureOpenAI


endpoint = os.getenv("ENDPOINT_URL", "https://midh2.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "d4c8f79efc774d6d88f952a2111d77bd")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint = endpoint,
    api_key = subscription_key,
    api_version = "2024-05-01-preview",
)

completion = client.chat.completions.create(
    model=deployment,
    messages= [
    {
        "role": "system",
        "content": "You are an AI assistant that helps people find information."
    },
    {
        "role": "user",
        "content": "hi"
    },
    {
        "role": "assistant",
        "content": "Hello! How can I assist you today?"
    },
    {
        "role": "user",
        "content": "im getting resource not found while making api call to you"
    },
    {
        "role": "assistant",
        "content": "I'm sorry, but I'm just an AI assistant and I don't have an API that you can call. However, if you provide me with more details about the API you're trying to use and the error message you're receiving, I may be able to help you troubleshoot the issue."
    },
    {
        "role": "user",
        "content": "im calling you"
    },
    {
        "role": "assistant",
        "content": "I see. Can you please clarify how you are trying to call me? Are you using a specific platform or service that interacts with an AI assistant like me?"
    },
    {
        "role": "user",
        "content": "yes"
    },
    {
        "role": "assistant",
        "content": "Can you please provide more information about the platform or service that you are using to interact with me? This will help me better understand the issue you are facing and provide you with the appropriate assistance."
    },
    {
        "role": "user",
        "content": "vscode"
    },
    {
        "role": "assistant",
        "content": "I see. Are you using a specific extension or tool within VS Code that interacts with an AI assistant like me? If so, please let me know the name of the extension or tool."
    }
],
    
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

print(completion.to_json())