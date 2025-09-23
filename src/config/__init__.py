from pathlib import Path

from .loader import load_config

conf = load_config()

LOCAL_FILE_DIR = Path(conf["service"]["storage"]["local"]["base_dir"])
LOG_BASE_DIR = Path(conf["service"]["log"]["base_dir"])