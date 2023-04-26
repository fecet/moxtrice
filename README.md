# Moxtrice

A simple tool to synchronize between moxfield.com and cockatrice

# Installation

Clont it and `pip install .` or simply

```
pip install moxtrice
```

# Usage

To get started, simply run the following command:
```
moxtrice
```
By default, Moxtrice will download all public lists for the default user [(me)](https://www.moxfield.com/users/Facet) into the current directory. You can override this by specifying a different username:
```
moxtrice --config.usernmae Yourname
```
Moxtrice will create a config file if you don't already have one. The config file looks like this:

```
decks:
- rMUqj1P1FEibzEFgpKqtSA
- uIbk-vrQjkaxqo_be_FFnQ
- -u5QNxgKb0uaU9t8vzztig
- C5hPo-DBXEa1uoibleNyTg
- jOPwBWIhokyYe8sjfcG3fA
- 3-GvVXtlgkWPmarhFwxphg
- Upa29gKDwES3C9InEcPUzw
- F8tbsl4bT0ObYoJyPQGyyA
- 6KIIGaY0G0ek6Dauhj5y-g
username: facet
```
Where the code are the string follows "https://www.moxfield.com/decks/" in your decklist url.

All synchronized lists are those defined in decks and all public decks from the specified user. This allows you to follow others and stay up to date.

To change the directory where the downloaded decks are saved, use the following command:
```
moxtrice --deckpath "path/to/yourdirectory"
```

# Configuration

You can modify the config file to change various settings, such as the username and the list of decks to synchronize. For example:

```
decks:
- rMUqj1P1FEibzEFgpKqtSA
- C5hPo-DBXEa1uoibleNyTg
- Upa29gKDwES3C9InEcPUzw
username: Yourname
```

the config file named `.moxtrice.yml` in your home directory("C:/Users/username" in Windows and "/home/usernmae" in unix-like).

You can also leave decks empty by:
```
decks: []
```

the config file named `.moxtrice.yml` in your home directory("C:/Users/username" in Windows and "/home/usernmae" in unix-like).


# Cautions

- Formats other than commander are supported, but they have not been thoroughly tested.
- Some dual-faced/transformed card names may be inconsistent between moxtrice and cockatrice.
- Currently, only public lists are supported because moxtrice's API is not public and we cannot really "login". According to [moxfield's FAQ](https://www.moxfield.com/help/faq#moxfield-api), this could be implemented if this project gets more attention and satisfies moxfield's requirements.

# Acknowledgments

Moxtrice would not be possible without the following resources:

- [moxfield](https://www.moxfield.com/)
- [cockatrice](https://cockatrice.github.io/)
- [MTG-TO-XMage](https://github.com/thebear132/MTG-To-XMage)
