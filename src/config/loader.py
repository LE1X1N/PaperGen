from pathlib import Path
import yaml


def load_config(config_path: str="config/dev.yaml"):
    """
        Load YAML config file
    """
    config_file = Path(config_path).resolve()
    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在：{config_file}")
    
    with open(config_file, "r") as f:
        return yaml.safe_load(f)