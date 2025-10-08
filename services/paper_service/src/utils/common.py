import json

def load_json(path):
    with open(path, "r", encoding='utf-8') as f:
        res = json.load(f)
    return res
