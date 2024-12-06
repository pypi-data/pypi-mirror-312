import requests
from tqdm import tqdm

from .path import get_zip_path
from .logger import logger


def download_zip():
    url = "https://miplib.zib.de/downloads/benchmark.zip"
    logger.info(f"Downloading from {url} to {get_zip_path()}")
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(get_zip_path(), 'wb') as file, \
         tqdm(
            desc="Downloading",
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

    logger.info(f"Downloaded to {get_zip_path()}")

def download_if_not_exists():
    if not get_zip_path().exists():
        download_zip()
    else:
        logger.info(f"Zip file already exists at {get_zip_path()}")