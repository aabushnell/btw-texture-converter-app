import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from convert import *

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.zip']
app.config['UPLOAD_PATH'] = 'packs/input'
app.config['DOWNLOAD_PATH'] = 'packs/output'

filename = ''

@app.route('/')
def index():  # render main page html
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    clear_input_folder()
    clear_output_folder()
    uploaded_file = request.files['file']
    global filename
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        convert()
    return redirect(url_for('download_file'))

@app.route('/download')
def download_file():
    return send_from_directory(app.config['DOWNLOAD_PATH'],
                               filename)

if __name__ == '__main__':
    app.run()
