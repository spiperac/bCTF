import yaml
import os
from django.conf import settings


config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config/config.yml")
config_schema = """
ctf:
  end_time: null
  logo: null
  start_time: null
  theme: null
  title: null
docker:
  driver: null
  host: null
  name: null
  password: null
  username: null
"""

def update_config(new_cfg):
    with open(config_file, 'w') as ymlfile:
        yaml.dump(new_cfg, ymlfile, default_flow_style=False)

def read_config():
    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    
    return cfg

def clear_config():
    with open(config_file, 'w') as ymlfile:
        yaml.dump(yaml.load(config_schema), ymlfile, default_flow_style=False)

def reload_settings():
    setattr(settings, 'CONFIG_FILE', read_config())
