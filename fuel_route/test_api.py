import requests
import json
import os

# Make sure the env is loaded
from dotenv import load_dotenv
load_dotenv()

payload = {
    'start': [-74.0060, 40.7128],
    'end': [-118.2437, 34.0522]
}

print("Testing API endpoint: http://127.0.0.1:8000/api/route/")
print("Payload:", json.dumps(payload, indent=2))

try:
    response = requests.post('http://127.0.0.1:8000/api/route/', json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
