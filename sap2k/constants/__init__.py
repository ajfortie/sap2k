import json
import os

def load_json(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'r') as file:
        return json.load(file)

units = load_json('units.json')
sap_paths = load_json('sap_paths.json')
