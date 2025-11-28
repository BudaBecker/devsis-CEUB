"""Helper functions for interacting with the Culinary Recipes API."""

from __future__ import annotations

from typing import Any, Dict, List

import requests

API_BASE = "http://127.0.0.1:8000/api"
DEFAULT_TIMEOUT = 5


def list_recipes(api_base: str = API_BASE) -> List[Dict[str, Any]]:
    response = requests.get(f"{api_base}/recipes", timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_recipe(recipe_id: int, api_base: str = API_BASE) -> Dict[str, Any]:
    response = requests.get(f"{api_base}/recipes/{recipe_id}", timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


def create_recipe(payload: Dict[str, Any], api_base: str = API_BASE) -> Dict[str, Any]:
    response = requests.post(
        f"{api_base}/create-recipe",
        json=payload,
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def update_recipe(recipe_id: int, payload: Dict[str, Any], api_base: str = API_BASE) -> None:
    response = requests.put(
        f"{api_base}/edit-recipe/{recipe_id}",
        json=payload,
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()


def delete_recipe(recipe_id: int, api_base: str = API_BASE) -> None:
    response = requests.delete(
        f"{api_base}/delete-recipe/{recipe_id}",
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()
