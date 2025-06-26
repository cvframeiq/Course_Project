from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import numpy as np
import json
import uuid
import os
import cv2
import tensorflow as tf

app = Flask(__name__)
os.makedirs("uploadimages", exist_ok=True)

# Load model
model = tf.keras.models.load_model("models/plant_disease_detection_model.keras")

# Class labels
label = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
         'Blueberry___healthy', 'Cherry___Powdery_mildew', 'Cherry___healthy',
         'Corn___Cercospora_leaf_spot Gray_leaf_spot', 'Corn___Common_rust', 'Corn___Northern_Leaf_Blight',
         'Corn___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
         'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
         'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
         'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
         'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
         'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
         'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
         'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
         'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
         'Tomato___healthy']

# Load disease descriptions
with open("plant_disease.json", 'r') as file:
    plant_disease = json.load(file)

@app.route('/uploadimages/<path:filename>')
def uploaded_images(filename):
    return send_from_directory('uploadimages', filename)

@app.route('/')
def home():
    return render_template('index.html')

def extract_features(image):
    image = tf.keras.utils.load_img(image, target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

def is_leaf_present(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return False
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_pixels = cv2.countNonZero(mask)
    total_pixels = image.shape[0] * image.shape[1]
    green_ratio = green_pixels / total_pixels
    return green_ratio > 0.02  # 2% threshold

def model_predict(image_path):
    img = extract_features(image_path)
    prediction = model.predict(img)
    predicted_index = np.argmax(prediction)
    predicted_class = label[predicted_index]

    disease_info = next((item for item in plant_disease if item["name"] == predicted_class), None)
    return disease_info

@app.route('/upload/', methods=['POST'])
def uploadimage():
    if request.method == "POST":
        image = request.files['img']
        temp_name = f"uploadimages/temp_{uuid.uuid4().hex}_{image.filename}"
        image.save(temp_name)

        # Check if leaf is present
        if not is_leaf_present(temp_name):
            return render_template('index.html',
                                   result=False,
                                   error="No leaf detected. Please upload a valid leaf image.")

        prediction = model_predict(temp_name)
        return render_template('index.html',
                               result=True,
                               imagepath=url_for('uploaded_images', filename=temp_name[13:]),
                               prediction=prediction)
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
