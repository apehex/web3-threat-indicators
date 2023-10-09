import os.path

# DATA ########################################################################

def get_data_dir_path() -> str:
    """Returns the path to the directory containing the data files."""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), './data/')
