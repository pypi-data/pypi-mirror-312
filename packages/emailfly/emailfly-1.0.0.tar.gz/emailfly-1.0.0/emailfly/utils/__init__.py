# Import specific functions or classes to make them directly accessible
from .utils import validate_path, get_files_from_dir

# Optional: Define what should be imported with `from mailify.utils import *`
__all__ = [
    'validate_path',
    'get_files_from_dir'
]