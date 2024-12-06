import os 
from pathlib import Path

def get_miplib_benchmark_dir() -> Path:
    path_from_env = os.getenv("MIPLIB_BENCHMARK_DIR", None)
    if path_from_env is None:
        path = Path.home() / ".miplib_benchmark"
    else:
        path = Path(path_from_env)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_mps_files_dir() -> Path:
    path = get_miplib_benchmark_dir() / "mps_files"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_zip_path() -> Path:
    return get_miplib_benchmark_dir() / "benchmark.zip"
