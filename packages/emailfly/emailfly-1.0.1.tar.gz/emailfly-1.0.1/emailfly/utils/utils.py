"""
utils.py
module path (app.utils.utils)

Utility functions for the app
"""

import os
from typing import List
from pathlib import Path

def validate_path(input_path: str) -> Path:
    """Checks if given path exists

    Args:
        input_path (str): Input Path

    Raises:
        FileNotFoundError: If file/folder does not exist on the given path

    Returns:
        Path: Path object if file exists
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No such file or directory: '{input_path}'")
    
    path = Path(input_path)
    return path



def get_files_from_dir(input_path: str) -> List[Path]:
    """Fetch files from the directory

    Args:
        input_path (str): Input Path

    Raises:
        FileNotFoundError: If file/folder does not exist on the given path

    Returns:
        List[Path]: List of Path objects if file exists
    """
    
    dir = Path(input_path).glob('**/*')

    files = [each for each in dir if each.is_file()]
    return files

