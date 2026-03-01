import os
import requests
from dotenv import load_dotenv

# Load your token and model from the .env file
load_dotenv()
token = os.environ.get("HUGGINGFACE_TOKEN") or os.environ.get("HF_TOKEN")
model = os.environ.get("LLM_MODEL", "meta-llama/Llama-3.1-8B-Instruct")

print(f"Testing Model: {model}")
url = f"https://api-inference.huggingface.co/models/{model}/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# A very safe, standard payload
payload = {
    "model": model,
    "messages": [{"role": "user", "content": "Say hello world"}],
    "max_tokens": 250
}

response = requests.post(url, headers=headers, json=payload)

print(f"\nStatus Code: {response.status_code}")
if response.status_code != 200:
    print(f"🚨 RAW ERROR DETAILS:\n{response.text}")
else:
    print(f"✅ SUCCESS:\n{response.json()['choices'][0]['message']['content']}")