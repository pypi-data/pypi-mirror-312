import pathlib
import gzip
import polars as pl

from .logger import logger
from .path import get_mps_files_dir
from .metadata import load_instances_metadata

_instances_df = None
def get_instances(count: int = None) -> pl.DataFrame:
    global _instances_df
    if _instances_df is None:
        _instances_df = load_instances_metadata()
    if count is not None:
        _instances_df = _instances_df.head(count)
    return _instances_df

def get_instance_names() -> list[str]:
    df: pl.DataFrame = get_instances()
    return df["instance_name"].to_list()

def get_instance_path(instance_name: str) -> pathlib.Path:
    # use glob to find the instance path
    logger.info(f"Searching for instance {instance_name} in {get_mps_files_dir()}")
    mps_file_path = get_mps_files_dir() / f"{instance_name}.mps"
    # if the mps file exists, return it
    if mps_file_path.exists():
        logger.info(f"Found instance {instance_name} at {mps_file_path}")
        return mps_file_path
    
    # otherwise, search for .mps.gz
    mps_gz_file_path = get_mps_files_dir() / f"{instance_name}.mps.gz"
    if mps_gz_file_path.exists():
        logger.info(f"Found compressed instance {instance_name} at {mps_gz_file_path}")
        # unzip, write the unzipped file to instance_name.mps
        logger.info(f"Unzipping {mps_gz_file_path}")
        with gzip.open(mps_gz_file_path, "rb") as f:
            with open(mps_file_path, "wb") as f_out:
                f_out.write(f.read())
        return mps_file_path

    # if no instance is found, raise an error
    raise FileNotFoundError(f"Instance {instance_name} not found")

def get_instance_path_str(instance_name: str) -> str:
    return str(get_instance_path(instance_name))