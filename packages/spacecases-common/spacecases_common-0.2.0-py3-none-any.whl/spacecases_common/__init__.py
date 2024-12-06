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


CONSUMER_GRADE_COLOUR = 0xB0C3D9
INDUSTRIAL_GRADE_COLOUR = 0x5E98D9
MIL_SPEC_COLOUR = 0x4B69FF
RESTRICTED_COLOUR = 0x8847FF
CLASSIFIED_COLOUR = 0xD32CE6
COVERT_COLOUR = 0xEB4B4B
CONTRABAND_COLOUR = 0xE4AE39


class Grade(IntEnum):
    CONSUMER_GRADE = 0
    INDUSTRIAL_GRADE = 1
    MIL_SPEC = 2
    RESTRICTED = 3
    CLASSIFIED = 4
    COVERT = 5
    CONTRABAND = 6

    def __str__(self):
        return [
            "Consumer Grade",
            "Industrial Grade",
            "Mil-Spec",
            "Restricted",
            "Classified",
            "Covert",
            "Contraband",
        ][self.value]

    def get_color(self):
        return [
            CONSUMER_GRADE_COLOUR,
            INDUSTRIAL_GRADE_COLOUR,
            MIL_SPEC_COLOUR,
            RESTRICTED_COLOUR,
            CLASSIFIED_COLOUR,
            COVERT_COLOUR,
            CONTRABAND_COLOUR,
        ][self.value]


@dataclass
class Skin:
    formatted_name: str
    description: Optional[str]
    image_url: str
    grade: Grade
    min_float: float
    max_float: float
    price: int


def remove_skin_name_formatting(skin_name: str) -> str:
    skin_name = skin_name.lower()
    skin_name = skin_name.translate(str.maketrans("", "", string.punctuation))
    for char in [" ", "™", "★"]:
        skin_name = skin_name.replace(char, "")
    return skin_name.strip()
