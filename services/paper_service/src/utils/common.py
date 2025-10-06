import json

def load_structure_from_json(path):
    with open(path, "r", encoding='utf-8') as f:
        structure = json.load(f)
    return structure


load_structure_from_json("test/structure_test.json")