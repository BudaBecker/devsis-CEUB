from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db.database import DatabaseManager
from app.entities.recipe import Recipe


router = APIRouter(prefix="/api")
db = DatabaseManager()


class RecipePayload(BaseModel):
	name: str
	description: str = ""
	cuisine: str = ""
	ingredients: str = ""
	instructions: str = ""
	preparation_time: int = 0


@router.post("/create-recipe")
async def create_recipe(payload: RecipePayload) -> dict[str, int | str]:
	recipe = Recipe(
		id=None,
		name=payload.name,
		description=payload.description,
		cuisine=payload.cuisine,
		ingredients=payload.ingredients,
		instructions=payload.instructions,
		preparation_time=payload.preparation_time,
	)
	recipe_id = db.insert_recipe(recipe)
	return {"message": "recipe created", "id": recipe_id}


@router.put("/edit-recipe/{recipe_id}")
async def edit_recipe(recipe_id: int, payload: RecipePayload) -> dict[str, str]:
	recipe = Recipe(
		id=recipe_id,
		name=payload.name,
		description=payload.description,
		cuisine=payload.cuisine,
		ingredients=payload.ingredients,
		instructions=payload.instructions,
		preparation_time=payload.preparation_time,
	)
	if not db.update_recipe(recipe):
		raise HTTPException
	return {"message": "recipe updated"}


@router.delete("/delete-recipe/{recipe_id}")
async def delete_recipe(recipe_id: int) -> dict[str, str]:
	if not db.delete_recipe(recipe_id):
		raise HTTPException
	return {"message": "recipe deleted"}
