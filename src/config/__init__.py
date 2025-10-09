import yaml


def load_config():
    with open("conf/service_config.yaml") as f:
        base_config = yaml.safe_load(f)
    return base_config

conf = load_config()
