from flask import Flask, render_template, request
from vqa_api import get_vqa_answer
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        image = request.files['image']

        if image and question:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            answer = get_vqa_answer(image_path, question)

            image_url = '/' + image_path.replace("\\", "/")  # Web-safe path
            return render_template('index.html', image_url=image_url, question=question, answer=answer)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
