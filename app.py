import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory 

# -----------------
# CONFIGURATION
# -----------------

UPLOAD_FOLDER = 'uploads' 
# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'} 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Secret key is required for flash messages and session management
app.config['SECRET_KEY'] = 'your_strong_secret_key_for_security' 

# -----------------
# HELPER FUNCTIONS
# -----------------

def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create the uploads folder if it does not exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_file_list():
    """Returns a list of files in the upload folder."""
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        # Filter to show only files (ignoring potential subfolders)
        return [f for f in files if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    except Exception as e:
        # Use app.logger for logging errors
        app.logger.error(f'Error reading upload folder: {e}')
        flash('Server error retrieving file list.', 'danger')
        return []

# -----------------
# MAIN ROUTE (Upload + List)
# -----------------

@app.route('/', methods=['GET', 'POST'])
def main_page():
    # Handles both file uploads (POST) and displaying the list (GET)
    if request.method == 'POST':
        # Check if file is present in the request
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                flash('No file selected for upload', 'warning')
            elif not allowed_file(file.filename):
                flash('Disallowed file extension.', 'danger')
            else:
                filename = secure_filename(file.filename)
                try:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash(f'File "{filename}" successfully uploaded!', 'success')
                except Exception as e:
                    flash(f'Error saving file: {e}', 'danger')
        
        # Always redirect to the GET request after POST to prevent re-submission
        return redirect(url_for('main_page'))
            
    # For GET request: display the page and file list
    file_list = get_file_list()
    return render_template('index.html', files=file_list)

# -----------------
# ROUTES FOR SERVING FILES
# -----------------

@app.route('/download/<filename>')
def download_file(filename):
    """Allows the user to force-download the file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/view/<filename>')
def view_file(filename):
    """Serves files (e.g., for image display) without forced download."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# -----------------
# DELETE ROUTE
# -----------------

@app.route('/delete', methods=['POST'])
def delete_file():
    """Handles the file deletion request."""
    filename = request.form.get('filename')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if filename and os.path.exists(filepath):
        try:
            os.remove(filepath)
            flash(f'File "{filename}" successfully deleted.', 'info')
        except Exception as e:
            flash(f'Error deleting file: {e}', 'danger')
    else:
        flash(f'Error: File "{filename}" not found.', 'danger')

    # Redirect to the main page to update the list
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    # Set debug=False for production
    app.run(debug=True)
