import os
from openai import AzureOpenAI
import base64
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configuration
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")  # Load the API key from env variables
IMAGE_PATH = "./4.png"
encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

# Initialize Azure OpenAI client
client = AzureOpenAI(
  azure_endpoint="https://azureaistudio4617393508.openai.azure.com", 
  api_key=API_KEY, 
  api_version="2024-02-15-preview"
)

# Define the payload
response = client.chat.completions.create(
  model="gpt-4o",  # Model = should match the deployment name you chose for your model deployment
  messages=[
    {
      "role": "system",
      "content": """You are an AI assistant that helps people find information. You are a document entity extraction specialist. 
      Given a document, your task is to extract the text value of entities.
      - Generate null for missing entities."""
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "\n"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{encoded_image}"
          }
        },
        {
          "type": "text",
          "text": """extract the the following entities as JSON
          - invoice number
          - items (description, quantity, total)"""
        }
      ]
    }
  ],
  temperature=0.7,
  top_p=0.95,
  max_tokens=800,
  response_format={ "type": "json_object" }
)

# Handle the response as needed (e.g., print or process)
print(response.choices[0].message.content)
