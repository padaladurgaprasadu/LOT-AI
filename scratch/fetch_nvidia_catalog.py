import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")
print(f"Testing NVIDIA API Key: {api_key[:15]}...")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

url = "https://integrate.api.nvidia.com/v1/models"

try:
    res = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        models_data = res.json().get("data", [])
        print(f"Total NVIDIA Models Available: {len(models_data)}")
        models = [m["id"] for m in models_data]
        
        # Save to scratch file
        with open("scratch/available_nvidia_models.json", "w") as f:
            json.dump(models, f, indent=2)
        print("Saved model list to scratch/available_nvidia_models.json")
        
        # Print top matching models from user list
        target_keys = ["nemotron", "glm", "minimax", "mistral", "deepseek", "qwen", "gemma"]
        print("\nTarget Models Found in NVIDIA NIM Catalog:")
        for m in models:
            if any(k in m.lower() for k in target_keys):
                print(f"  • {m}")
    else:
        print(f"Error Response: {res.text}")
except Exception as e:
    print(f"Request failed: {e}")
