# %%

from copy import deepcopy
from dataclasses import dataclass, field
import html
import json
import logging
import os
import os
from pathlib import Path
import re
from tokenize import String
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests
from typing import *
from tqdm import tqdm
import time
from absl import app, flags, logging
from ml_collections import config_flags
import emoji

FLAGS = flags.FLAGS
card_name_exceptions = {"Brazen Borrower": "Brazen Borrower // Petty Theft"}
config_flags.DEFINE_config_file(
    "config",
    "config.py",
    "File path to the training hyperparameter configuration.",
    lock_config=False,
)

# %%


@dataclass
class MTGCard:
    name: str
    quantity: int

    @staticmethod
    def from_json(json: dict):
        pass
        # name.split(" // ")[0], attr["quantity"]
        # return MTGCard(json["name"], json["quantity"])


@dataclass
class DeckList:
    mainboard: List[MTGCard]
    name: str = ""
    description: str = ""
    format: str = ""
    companions: List[MTGCard] = field(default_factory=lambda: [])
    commanders: List[MTGCard] = field(default_factory=lambda: [])
    sideboard: List[MTGCard] = field(default_factory=lambda: [])
    maybeboard: List[MTGCard] = field(default_factory=lambda: [])
    tokens: List[MTGCard] = field(default_factory=lambda: [])

    def to_trice(self, trice_path=Path("decks")):
        trice_path.mkdir(parents=True, exist_ok=True)
        for card in self.companions + self.commanders:
            self.sideboard.append(card)
        to_trice(
            self.mainboard,
            self.sideboard,
            f"{self.format}-{self.name}",
            self.description,
            trice_path=trice_path,
        )


@dataclass
class MoxField:
    username: str = ""

    # xmageFolderPath = ""
    def getUserDecks(self):
        url = (
            "https://api.moxfield.com/v2/users/"
            + self.username
            + "/decks?pageNumber=1&pageSize=99999"
        )
        # Logging
        # print(f"Grabbing <{self.username}>'s public decks from " + url)
        r = requests.get(url)
        j = json.loads(r.text)
        # printJson(j)
        return j

    def getDecklist(self, deckId):
        # https://api.moxfield.com/v2/decks/all/g5uBDBFSe0OzEoC_jRInQw
        url = "https://api.moxfield.com/v2/decks/all/" + deckId
        # print(f"Grabbing decklist <{deckId}>")                        #Logging
        r = requests.get(url)
        jsonGet = json.loads(r.text)
        return jsonGet


def _pretty_print(current, parent=None, index=-1, depth=0):
    for i, node in enumerate(current):
        _pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = "\n" + ("\t" * depth)
        else:
            parent[index - 1].tail = "\n" + ("\t" * depth)
        if index == len(parent) - 1:
            current.tail = "\n" + ("\t" * (depth - 1))


def normlize_name(name):
    name = emoji.replace_emoji(name, "")
    name = re.sub(r"\\u[0-9a-fA-F]{4}", "", sanitize_filename(name))
    return name


def to_trice(
    mainboard_list: List[MTGCard],
    sideboard_list: List[MTGCard] = [],
    name="",
    description="",
    trice_path=Path("~/.local/share/Cockatrice/Cockatrice/decks"),
):
    root = ET.Element("cockatrice_deck")
    root.set("version", "1")

    deckname = ET.SubElement(root, "deckname")
    deckname.text = name

    comments = ET.SubElement(root, "comments")
    comments.text = description

    mainboard = ET.SubElement(root, "zone")
    mainboard.set("name", "main")

    for card in mainboard_list:
        card1 = ET.SubElement(mainboard, "card")
        card1.set("number", str(card.quantity))
        card1.set("name", card.name)

    sideboard = ET.SubElement(root, "zone")
    sideboard.set("name", "side")

    for card in sideboard_list:
        card1 = ET.SubElement(sideboard, "card")
        card1.set("number", str(card.quantity))
        card1.set("name", card.name)

    _pretty_print(root)
    tree = ET.ElementTree(root)
    # ET.indent(tree, space="\t", level=0)
    # trice_path=
    fp = trice_path / f"{normlize_name(name)}.cod"
    logging.error(f"Writing to {fp}")
    tree.write(fp, encoding="UTF-8", xml_declaration=True)


def to_cards(raw_cards: dict) -> List[MTGCard]:
    cards = [
        MTGCard(name.split(" // ")[0], attr["quantity"])
        for name, attr in raw_cards.items()
    ]
    return cards


# %%


def main(agrv):
    config = FLAGS.config
    client = MoxField(config.username)
    deck_ids = [j["publicId"] for j in client.getUserDecks()["data"]]

    if config.decks:
        deck_ids = list(set(config.decks) + set(deck_ids))

    jsonGets = []
    for deck in tqdm(deck_ids, desc="Getting data from moxfield"):
        logging.info(f"Grabbing decklist <{deck}>")
        jsonGet = client.getDecklist(deck)
        jsonGets.append(jsonGet)
        time.sleep(0.5)

    for jsonGet in tqdm(jsonGets, desc="Converting deck to trice"):
        name = jsonGet["name"]
        description = jsonGet["description"]
        mainboard_list = to_cards(jsonGet["mainboard"])
        sideboard_list = to_cards(jsonGet["sideboard"])
        # jsonGet['tokens']
        commanders = to_cards(jsonGet["commanders"])
        companions = to_cards(jsonGet["companions"])
        format = jsonGet["format"]
        # time.sleep(0.5)
        DeckList(
            mainboard_list,
            name,
            description,
            format,
            sideboard=sideboard_list,
            commanders=commanders,
            companions=companions,
        ).to_trice()


if __name__ == "__main__":
    app.run(main)
