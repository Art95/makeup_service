import os
from pathlib import Path


def get_data_folder():
    root_folder = Path(__file__).parent.parent
    data_folder = os.path.join(root_folder, 'data')

    return data_folder
