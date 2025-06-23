from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from Generator import generate_post  # Modified version of your on_generate logic

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    generated_post = ""
    image_url = None
    if request.method == "POST":
        prompt = request.form.get("prompt")

        image = request.files.get("image")
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = url_for("static", filename=f"uploads/{filename}")
        else:
            image_path = ""

        generated_post = generate_post(prompt, image_path)

    return render_template("index.html", generated_post=generated_post, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
