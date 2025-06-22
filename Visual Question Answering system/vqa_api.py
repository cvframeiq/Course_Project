# vqa_api.py

import requests
import base64
import json
from PIL import Image
import os

def get_vqa_answer(image_path, question):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    headers = {
        "Authorization": "Bearer THE-API-KEY",  # Replace safely via environment in Flask
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                             headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        answer = result['choices'][0]['message']['content']
        return answer
    else:
        print(f"[Error] Status Code: {response.status_code}")
        print(response.text)
        return None
