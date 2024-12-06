from fgi_yaml_formattor import (dump_to_yaml)
from yaml import safe_load
print(dump_to_yaml(safe_load(open('tests/example.yaml'))))