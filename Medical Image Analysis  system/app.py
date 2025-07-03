from flask import Flask, render_template, request, redirect, url_for
from vqa_api import get_vqa_answer
import os
from werkzeug.utils import secure_filename

# Creating Flask app
app = Flask(__name__)

# Folder where uploaded images will be stored
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#homepage route
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#handles the form submission
@app.route('/result', methods=['POST'])
def result():
    question = request.form['question']
    image = request.files['image']

#Check if both question and image are provided
    if image and question:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

         # Call VQA function to get the answer
        answer = get_vqa_answer(image_path, question)

        # Creating a web-safe path
        image_url = '/' + image_path.replace("\\", "/") 

        return render_template('index.html', image_url=image_url, question=question, answer=answer)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
