import requests
import base64
import json
import os
from PIL import Image
import matplotlib.pyplot as plt

image_extensions = ('.png', '.jpg', '.jpeg')
image_files = [f for f in os.listdir('.') if f.lower().endswith(image_extensions)]

if not image_files:
    print("No image files found in the current folder.")
    exit()

print("Available images:")
for fname in image_files:
    print(f"- {fname}")

image_path = input("Enter the image filename to use (e.g., example.jpg): ").strip()

if not os.path.isfile(image_path):
    print("File not found. Please check the filename.")
    exit()


with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")


question = input("Enter your question about the image: ")


headers = {
    "Authorization": "Bearer THE-API-KEY",  
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

    image = Image.open(image_path)
    plt.figure(figsize=(6, 6))
    plt.title(f"Q: {question}\nA: {answer}", fontsize=12)
    plt.imshow(image)
    plt.axis("off")
    plt.show()
else:
    print(f"[Error] Status Code: {response.status_code}")
    print(response.text)
