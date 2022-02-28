import os
from flask import render_template
from pathlib import Path
from util import get_uploads_folder_url


def file_upload_page():
    return render_template('file_upload.html')


def file_upload_api(request, app):
    file = request.files['file']
    saved_file_result = _save_temp_file(file, app)
    saved_file_path = saved_file_result['saved_path']

    file_name = Path(saved_file_path).name

    public_upload_file_path = os.path.join(app.config['PUBLIC_UPLOAD_FOLDER'], file_name)
    
    os.system(f'mv {saved_file_path} {public_upload_file_path}')

    return {
        'saved_file_path': f'{get_uploads_folder_url()}/{file_name}'
    }


def _save_temp_file(file, app):
    original_file_name = file.filename
    temp_upload_file_path = os.path.join(app.config['TEMP_UPLOAD_FOLDER'], original_file_name)
    resized_image_path = f'{temp_upload_file_path}.min.png'
    file.save(temp_upload_file_path)

    # https://imagemagick.org/script/convert.php
    os.system(f'magick {temp_upload_file_path} -resize 50% {resized_image_path}')

    return {
        'saved_path': resized_image_path
    }