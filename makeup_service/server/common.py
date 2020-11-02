import os
from pathlib import Path


def get_uploads_folder_path():
    return os.path.join(Path(__file__).parent, 'uploads')


def get_data_folder():
    root_folder = Path(__file__).parent.parent.parent
    data_folder = os.path.join(root_folder, 'data')

    return data_folder
