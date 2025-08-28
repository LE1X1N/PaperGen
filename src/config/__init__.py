from pathlib import Path

from .loader import load_config

conf = load_config()

LOCAL_FILE_DIR = Path(conf["service"]["local_file_dir"])
LOG_BASE_DIR = Path(conf["service"]["log"]["base_dir"])