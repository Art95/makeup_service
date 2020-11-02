import os
from pathlib import Path


def get_uploads_folder_path():
    return os.path.join(Path(__file__).parent, 'uploads')
