import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

print("Testing API key and finding available models...")
print(f"API Key: {api_key[:20]}...")

# Test different endpoints
endpoints = [
    f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
    f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
]

for endpoint in endpoints:
    print(f"\nTrying: {endpoint[:80]}...")
    try:
        r = requests.get(endpoint)
        if r.status_code == 200:
            data = r.json()
            print("✅ SUCCESS! Available models:")
            if 'models' in data:
                for model in data['models']:
                    name = model.get('name', 'Unknown')
                    methods = model.get('supportedGenerationMethods', [])
                    if 'generateContent' in methods:
                        print(f"  - {name}")
            break
        else:
            print(f"❌ Failed: {r.status_code} - {r.text[:200]}")
    except Exception as e:
        print(f"❌ Error: {e}")
