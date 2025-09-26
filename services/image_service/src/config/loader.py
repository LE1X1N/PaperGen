import yaml

def load_yaml(file_path: str):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def load_config():
    """
        Load YAML config file
    """
    base_config = load_yaml("conf/service_config.yaml")
    return base_config
