import os
from pathlib import Path


def get_test_files_folder_path():
    tests_root_folder = Path(__file__).parent.parent
    test_files_folder = os.path.join(tests_root_folder, 'files')

    return test_files_folder
