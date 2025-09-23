from pathlib import Path

from .loader import load_config

conf = load_config()
LOG_BASE_DIR = Path(conf["service"]["log"]["base_dir"])