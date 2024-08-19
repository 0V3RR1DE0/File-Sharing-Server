from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file.save(filename)
        flash('File uploaded successfully', 'success')
        return redirect(url_for('index'))

@app.route('/files/')
@app.route('/files/<path:subpath>')
def list_files(subpath=''):
    current_path = os.path.join(UPLOAD_FOLDER, subpath)
    if not os.path.exists(current_path):
        flash('Folder not found', 'error')
        return redirect(url_for('list_files'))

    items = os.listdir(current_path)
    folders = [item for item in items if os.path.isdir(os.path.join(current_path, item))]
    files = [item for item in items if os.path.isfile(os.path.join(current_path, item))]
    
    return render_template('files.html', subpath=subpath, folders=folders, files=files)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
