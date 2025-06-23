
import base64
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
print("API Key:", API_KEY)  # Debug line

def generate_post(prompt, image_path):
    if not image_path:
        return "[Error] No image provided."

    try:
        with open(image_path, "rb") as f:
            base64_img = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        return f"[Error reading image] {e}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers,
                                 data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"[API Error {response.status_code}]\n{response.text}"
    except Exception as e:
        return f"[Request Failed] {e}"
