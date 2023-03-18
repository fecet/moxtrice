# %%
from pathlib import Path
import time
from typing import *

from absl import app, flags, logging
from ml_collections import config_flags
from tqdm import tqdm
from .core import MoxField, DeckList
from ._version import __version__
from .utils import redirect_to_tqdm

FLAGS = flags.FLAGS
card_name_exceptions = {"Brazen Borrower": "Brazen Borrower // Petty Theft"}
config_flags.DEFINE_config_file(
    "config",
    str(Path(__file__).parent / "config.py"),
    "File path to the training hyperparameter configuration.",
    lock_config=False,
)

flags.DEFINE_boolean("version", False, "Prints the version of the program and exits.")

flags.DEFINE_boolean("dryrun", False, "Test without writing to computer.")

flags.DEFINE_string("deckpath", "", "Where to save decklists")


def main(agrv):
    config = FLAGS.config

    if FLAGS.version:
        return print(__version__)

    client = MoxField(config.username)
    deck_ids = []
    if config.username:
        deck_ids = [j["publicId"] for j in client.getUserDecks()["data"]]
    if config.decks:
        deck_ids = list(set(config.decks+deck_ids))

    config_fp = Path.home() / ".moxtrice.yml"
    if not config_fp.exists():
        config.decks = deck_ids
        with open(config_fp, "w") as f:
            f.write(repr(config))

    jsonGets = []
    with redirect_to_tqdm(tqdm):
        for deck in tqdm(deck_ids, desc="Getting data from moxfield"):
            logging.debug(f"Grabbing decklist <{deck}>")
            jsonGet = client.getDecklist(deck)
            jsonGets.append(jsonGet)
            # time.sleep(0.5)

        if not FLAGS.dryrun:
            for jsonGet in tqdm(jsonGets, desc="Converting deck to trice"):
                decklist = DeckList.from_json(jsonGet)
                decklist.to_trice(Path(FLAGS.deckpath))


def absl_main():
    return app.run(main)


if __name__ == "__main__":
    absl_main()
