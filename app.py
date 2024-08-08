from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Set a secret key for flash messages

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))

    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flash('File uploaded successfully', 'success')
        return redirect(url_for('index'))

@app.route('/files')
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('files.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
