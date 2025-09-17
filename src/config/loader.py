import yaml
import os

from deepmerge import Merger

ENV = os.getenv("APP_ENV", "prod")

def load_yaml(file_path: str):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def load_config():
    """
        Load YAML config file
    """
    merger = Merger([(dict, "merge")], [], [])
    
    base_config = load_yaml("config/base.yaml")
    ext_config = load_yaml(f"config/config_{ENV}.yaml")
    final_config = merger.merge(base_config, ext_config)
    return final_config
