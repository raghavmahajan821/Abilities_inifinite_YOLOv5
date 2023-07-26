from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict(img_path):
    os.system(f"python yolov5/detect.py --weights best.pt --conf 0.4 --source {img_path}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:  #
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':          # if no file selected
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # secure file size
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(r"static\process\exp"):
            shutil.rmtree(r"static\process\exp", ignore_errors=True)
        file.save(path)    # photo will get saved in static
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    os.system(f'python yolov5/detect.py --weights best.pt --conf 0.4 --source {os.path.join(app.config["UPLOAD_FOLDER"], filename)}')
    import time
    time.sleep(20)
    os.system("move ./yolov5/runs/detect/exp ./static/process/exp")
    return redirect(url_for('static', filename=f"../static/process/exp/{filename}"))

if __name__ == "__main__":
    app.run(debug=True)


