from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# In-memory storage for our simulated files
files_storage = {
    'example.txt': {
        'name': 'example.txt',
        'size': '12 KB',
        'upload_date': '2023-05-15',
        'last_modified': '2023-05-15'
    }
}

@app.route('/')
def index():
    return render_template('index.html', files=files_storage)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file_name = request.form.get('file_name')
        file_size = request.form.get('file_size') or '0 KB'
        
        if not file_name:
            flash('File name is required!', 'error')
            return redirect(url_for('upload'))
        
        secure_name = secure_filename(file_name)
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        files_storage[secure_name] = {
            'name': secure_name,
            'size': file_size,
            'upload_date': current_date,
            'last_modified': current_date
        }
        
        flash(f'File "{secure_name}" uploaded successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('upload.html')

@app.route('/update/<filename>', methods=['GET', 'POST'])
def update(filename):
    if filename not in files_storage:
        flash('File not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_name = request.form.get('new_name')
        
        if not new_name:
            flash('New file name is required!', 'error')
            return redirect(url_for('update', filename=filename))
        
        secure_new_name = secure_filename(new_name)
        
        if secure_new_name != filename:
            # Remove old entry and create new one
            file_data = files_storage.pop(filename)
            file_data['name'] = secure_new_name
            file_data['last_modified'] = datetime.now().strftime('%Y-%m-%d')
            files_storage[secure_new_name] = file_data
        
        flash(f'File updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('update.html', file=files_storage[filename])

@app.route('/delete/<filename>')
def delete(filename):
    if filename in files_storage:
        files_storage.pop(filename)
        flash(f'File "{filename}" deleted successfully!', 'success')
    else:
        flash('File not found!', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)