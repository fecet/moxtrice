from ml_collections import ConfigDict
from pathlib import Path
import yaml

def get_config():
    config = ConfigDict()
    config.username = "facet"
    config.decks = []

    config_fp = Path.home() / ".moxtrice.yml"
    if config_fp.exists():
        with open(config_fp,"r") as f:
            conf=yaml.load(f.read(), yaml.UnsafeLoader)
        config.update(conf)

    return config
