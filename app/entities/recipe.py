from dataclasses import dataclass


@dataclass
class Recipe:
    id: int | None
    name: str
    description: str
    cuisine: str
    ingredients: str
    instructions: str
    preparation_time: int # minutes
