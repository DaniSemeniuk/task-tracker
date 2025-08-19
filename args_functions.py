"""functions for the CLI arguments"""

import json


def dump(data):
    with open("DB.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
    return


def add():
    pass
