import os
import shutil
import video_processing

from flask import Flask, request, render_template, send_file

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

@app.route('/')
def upload_form():
    return render_template('upload_form.html')

@app.route('/process', methods=['POST'])
def process_files():
    option = request.form['option']
    file = request.files.get('file')

    if option not in ['1', '2', '3', '4', '5']:
        return 'Invalid option'

    if  not file:
        return 'No files selected'

    # Save the uploaded files
    file_path = None

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

    # Process the uploaded files based on the selected option
    processed_file_path = None

    if option == '1':
        # Process audio file
        processed_file_path = video_processing.process_video_audio(file_path)
    elif option == '2':
        # Process video file
        processed_file_path = video_processing.process_video_text(file_path)
    elif option == '3':
        # Process video file
        processed_file_path = video_processing.process_audio_text(file_path)
    elif option == '4':
        # Process video file
        processed_file_path = video_processing.process_video_subvideo(file_path)
    elif option == '5':
        # Process video file
        processed_file_path = video_processing.process_video_transvideo(file_path)
    # Add more elif blocks for other options...

    if processed_file_path:
        # Return a link to download the processed file
        return f'Files processed successfully. <a href="/download/{os.path.basename(processed_file_path)}">Download processed file</a>'
    else:
        return 'File processing failed'

@app.route('/download/<filename>')
def download_file(filename):
    processed_file_path = os.path.join(PROCESSED_FOLDER, filename)
    return send_file(processed_file_path, as_attachment=True)

if __name__ == '__main__':
    # Ensure that the upload and processed folders exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    app.run(debug=True)
