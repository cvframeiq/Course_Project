# Visual Question Answering (VQA) using OpenRouter API

This project allows users to ask natural language questions about any image using OpenRouter's GPT-4o API.

## Features

- Upload an image and ask a question about it
- Get intelligent answers from GPT-4o (Vision model)
- Image preview with question + answer

## Requirements

- Python 3.10+
- Install dependencies:
  ```bash
  pip install requests matplotlib pillow

## How to Use

- Put your image (e.g., example.jpg) in the project folder
- Replace "THE-API-KEY" in vqa_api.py with your OpenRouter API key
- Run the app:
  ```bash
  python vqa_api_app.py
Follow the prompts to enter the image filename and your question

## Screenshot

![VQA Screenshot](screenshot1.png)

![VQA Screenshot](screenshot2.png)
