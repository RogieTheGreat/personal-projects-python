import pickle
from dataclasses import dataclass, field
from typing import List
import json

MAX_RESTO = 30
MAX_DISH = 7
DATA_FILE = "data.pkl"


@dataclass
class Menu:
    name: str
    type: str
    price: float


@dataclass
class Restaurant:
    name: str
    city: str
    tel: str
    rating: int
    dishes: List[Menu] = field(default_factory=list)


def main():
    print("Restaurant system loaded")


def load_restaurants():
    try:
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []


def save_restaurants(restos):
    # KEEP pickle (no change to app)
    with open(DATA_FILE, "wb") as f:
        pickle.dump(restos, f)

    # ALSO save JSON
    data = []

    for r in restos:
        data.append({
            "name": r.name,
            "city": r.city,
            "tel": r.tel,
            "rating": r.rating,
            "dishes": [
                {
                    "name": d.name,
                    "type": d.type,
                    "price": d.price
                }
                for d in r.dishes
            ]
        })

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


def valid_tel(tel):
    return tel.isdigit() and len(tel) >= 8


def format_name(name):
    return name.strip().title()


def valid_rating(rating):
    return isinstance(rating, int) and 1 <= rating <= 5


if __name__ == "__main__":
    main()
