import os 
from pathlib import Path
def file_exists_in_current_dir(file_name):
    current_dir = Path.cwd()
    file_path = current_dir / file_name
    return file_path.exists()

print(file_exists_in_current_dir("k"))