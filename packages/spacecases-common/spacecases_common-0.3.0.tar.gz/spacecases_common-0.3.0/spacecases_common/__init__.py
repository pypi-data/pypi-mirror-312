import string
from enum import IntEnum
from dataclasses import dataclass
from typing import Optional


class Condition(IntEnum):
    FACTORY_NEW = 0
    MINIMAL_WEAR = 1
    FIELD_TESTED = 2
    WELL_WORN = 3
    BATTLE_SCARRED = 4

    def __str__(self):
        return [
            "Factory New",
            "Minimal Wear",
            "Field-Tested",
            "Well-Worn",
            "Battle-Scarred",
        ][self.value]


@dataclass
class Skin:
    formatted_name: str
    description: Optional[str]
    image_url: str
    grade: str
    min_float: float
    max_float: float
    price: int


def remove_skin_name_formatting(skin_name: str) -> str:
    skin_name = skin_name.lower()
    skin_name = skin_name.translate(str.maketrans("", "", string.punctuation))
    for char in [" ", "™", "★"]:
        skin_name = skin_name.replace(char, "")
    return skin_name.strip()
