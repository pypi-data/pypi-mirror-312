import string
from dataclasses import dataclass
from typing import Optional


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
