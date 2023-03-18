from moxtrice import MoxField, DeckList, MTGCard
import yaml

from ml_collections import ConfigDict

def get_config():
    config = ConfigDict()
    config.username = "facet"
    config.decks = []
    return config

# %%
config = get_config()
# client = MoxField(config.username)
# deck_ids = [j["publicId"] for j in client.getUserDecks()["data"]]
# config.decks = deck_ids
#
# with open("moxtrice.yml","w") as f:
#     f.write(repr(config))
    
print(config)

with open("moxtrice.yml","r") as f:
    conf=yaml.load(f.read(), yaml.UnsafeLoader)

config.update(conf)
print(config)
