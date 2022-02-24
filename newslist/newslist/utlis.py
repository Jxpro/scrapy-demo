import json
from os.path import dirname, realpath


def get_config(name):
    path = dirname(realpath(__file__)) + '/configs/%s.json' % name
    with open(path, encoding='utf-8') as f:
        return json.load(f)
