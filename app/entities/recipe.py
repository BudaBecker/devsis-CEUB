from dataclasses import dataclass

@dataclass
class Recipe:
    """A dataclass to represent a culinary recipe."""
    id: int
    name: str
    description: str
    cuisine: str
    ingredients: str
    instructions: str
    preparation_time: int # minutes
