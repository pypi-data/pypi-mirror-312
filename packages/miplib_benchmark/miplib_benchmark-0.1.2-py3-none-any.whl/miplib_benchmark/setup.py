from .download import download_if_not_exists
from .unzip import unzip_if_empty

def setup():
    download_if_not_exists()
    unzip_if_empty()
