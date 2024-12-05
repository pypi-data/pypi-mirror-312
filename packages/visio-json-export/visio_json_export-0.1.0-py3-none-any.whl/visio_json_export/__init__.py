import json
from .visio_model import VisioModel


def load_file(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return VisioModel(**data)


def load_string(json_string):
    data = json.loads(json_string)
    return VisioModel(**data)