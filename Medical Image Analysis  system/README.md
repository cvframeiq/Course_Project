# Medical Image Analysis System using OpenRouter API

This project is a simple web application that allows users to upload an medical image and ask natural language questions about it. The system uses OpenRouter's GPT-4o Vision model to generate intelligent answers based on the visual content.

---

## Features

- Upload any medical image through the web interface  
- Ask natural language questions about the image  
- Get accurate visual answers powered by GPT-4o (Vision)  
- Display the image along with the question and model's answer  

---

## Tech Stack

- Frontend: HTML(via Flask)
- Backend: Python (Flask framework)  
- Model API: [OpenRouter GPT-4o Vision](https://openrouter.ai/)  
- Others: `requests`, `Pillow`, `matplotlib`, `os`, `base64`  

---

## Requirements

- Python 3.10+  
- Install required libraries:

  ```bash
  pip install flask requests matplotlib pillow
  ```

---

## How to Run

- Clone or download this repository  
- Add your image(s) to the `static/uploads/` folder, or upload them via the web UI  
- Set your API key:  
  - Open `vqa_api.py`  
  - Replace `"THE-API-KEY"` with your actual OpenRouter API key  
- Run the Flask app:

  ```bash
  cd "Medical Image Analysis system"
  python app.py
  ```

- Visit the app in your browser:  
  Open browser at http://localhost

---

## Screenshot

![VQA Screenshot](static/uploads/Output_blood_report.png)
![VQA Screenshot](static/uploads/medicine_Output.png)
