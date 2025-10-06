import sqlite3
from typing import List, Optional
from app.entities.recipe import Recipe

class DatabaseManager:
    def __init__(self):
        self.db_path = "app/db/recipes.db"
        self.conn = None
        self.setup_database()
    
    def setup_database(self):
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                cuisine TEXT,
                ingredients TEXT,
                instructions TEXT,
                preparation_time INTEGER
            )
        ''')
        self.conn.commit()

    def insert_recipe(self, recipe: Recipe) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO recipes (name, description, cuisine, ingredients, 
                               instructions, preparation_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (recipe.name, recipe.description, recipe.cuisine, recipe.ingredients,
              recipe.instructions, recipe.preparation_time))
        self.conn.commit()
        return cursor.lastrowid

    def update_recipe(self, recipe: Recipe) -> bool:
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE recipes 
            SET name=?, description=?, cuisine=?, ingredients=?, 
                instructions=?, preparation_time=?
            WHERE id=?
        ''', (recipe.name, recipe.description, recipe.cuisine, recipe.ingredients,
              recipe.instructions, recipe.preparation_time, recipe.id))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_recipe(self, recipe_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM recipes WHERE id=?', (recipe_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_recipe(self, recipe_id: int) -> Optional[Recipe]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM recipes WHERE id=?', (recipe_id,))
        row = cursor.fetchone()
        if row:
            return Recipe(*row)
        return None

    def get_all_recipes(self) -> List[Recipe]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM recipes')
        return [Recipe(*row) for row in cursor.fetchall()]

    def __del__(self):
        if self.conn:
            self.conn.close()
