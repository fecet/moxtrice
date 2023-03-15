from ml_collections import ConfigDict

def get_config():
    config = ConfigDict()
    config.username = "facet"
    config.decks = []
    return config
