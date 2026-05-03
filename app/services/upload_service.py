import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def salvar_arquivo(arquivo):
    if not arquivo:
        return None
    
    # Save inside app/static/uploads
    upload_folder = os.path.join('app', 'static', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    filename = secure_filename(arquivo.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    path = os.path.join(upload_folder, unique_filename)
    arquivo.save(path)
    
    # Return only the filename to be stored in DB
    return unique_filename
