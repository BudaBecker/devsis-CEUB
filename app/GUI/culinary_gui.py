# Native imports
import tkinter as tk
from tkinter import ttk

# Installed imports
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# Local imports
from app.entities.recipe import Recipe
from app.db.database import DatabaseManager
from app.gui.recipes_list import RecipeList
from app.gui.form import Form


class CulinaryGUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.db = DatabaseManager()
        self.title("Culinary Recipes — CRUD App")
        self.iconbitmap('app/img/app_icon.ico')
        self.geometry("1200x720")
        self.minsize(1000, 600)
        
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True)
        
        self.frames = {}
        
        for F in (RecipeList, Form):
            page_name = F.__name__
            frame = F(parent=main, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.style = tb.Style()

        # Removing selected button overlay
        self.style.layout(
            "TButton",
            [
                ("Button.border", {"sticky": "nswe", "children": [
                    ("Button.padding", {"sticky": "nswe", "children": [
                        ("Button.label", {"sticky": "nswe"})
                    ]})
                ]})
            ]
        )

        # Root grid weights for responsive resizing
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(2, weight=1)
        self.app.grid_rowconfigure(3, weight=0)
        
        self._create_header()
        self._create_main_content()
        self._create_status_bar()
        self._setup_event_handlers()

        self.current_recipe = None

    def _create_header(self):
        header = tb.Frame(self.app, padding=(16, 12))
        header.grid(row=0, column=0, sticky=EW)
        title_lbl = tb.Label(header, text="Culinary Recipes ", font=("Segoe UI", 18, "bold"))
        subtitle_lbl = tb.Label(header, text="A modern culinary recipes book", bootstyle=SECONDARY)
        title_lbl.grid(row=0, column=0, sticky=W)
        subtitle_lbl.grid(row=1, column=0, sticky=W)

    def _create_main_content(self):
        # --- Main Content: Left (Form) & Right (Table) ---------------------------
        main = tb.Frame(self.app, padding=(16, 8, 16, 16))
        main.grid(row=2, column=0, sticky=NSEW)
        main.grid_columnconfigure(0, weight=0)  # form column fixed
        main.grid_columnconfigure(1, weight=1)  # table column expands
        main.grid_rowconfigure(0, weight=1)

        


    def _create_status_bar(self):
        status = tb.Frame(self.app, padding=(16, 6))
        status.grid(row=3, column=0, sticky=EW)
        self.status_lbl = tb.Label(status, text="Ready • No recipe selected", bootstyle=SECONDARY)
        self.status_lbl.pack(side=LEFT)

    def _setup_event_handlers(self):
        self.create_btn.config(command=self._create_recipe)
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

    def _clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.cuisine_cb.set('')
        self.prep_sp.delete(0, tk.END)
        self.prep_sp.insert(0, '0')
        self.description_txt.delete('1.0', tk.END)
        self.ingredients_txt.delete('1.0', tk.END)
        self.steps_txt.delete('1.0', tk.END)
        self.current_recipe = None
        self.create_btn.config(text="Create")

    def _load_recipes(self):
        self.tree.delete(*self.tree.get_children())
        for recipe in self.db.get_all_recipes():
            display_desc = (recipe.description[:200] + "...") if len(recipe.description) > 200 else recipe.description
            tag = "evenrow" if recipe.id % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(recipe.id, recipe.name, display_desc, 
                           recipe.cuisine, recipe.preparation_time), tags=(tag,))

    def _create_recipe(self):
        name = self.name_entry.get().strip()
        cuisine = self.cuisine_cb.get().strip()
        prep = int(self.prep_sp.get().strip() or 0)
        description = self.description_txt.get("1.0", "end").strip()
        ingredients = self.ingredients_txt.get("1.0", "end").strip()
        instructions = self.steps_txt.get("1.0", "end").strip()

        if not name:
            self.status_lbl.config(text="Name is required")
            return

        recipe = Recipe(
            id=getattr(self.current_recipe, 'id', None),
            name=name,
            description=description,
            cuisine=cuisine,
            ingredients=ingredients,
            instructions=instructions,
            preparation_time=prep
        )

        if self.current_recipe:
            self.db.update_recipe(recipe)
            self.status_lbl.config(text=f"Updated recipe: {name}")
        else:
            recipe_id = self.db.insert_recipe(recipe)
            self.status_lbl.config(text=f"Added recipe #{recipe_id}: {name}")

        self._clear_form()
        self._load_recipes()

    def _edit_recipe(self):
        selected = self.tree.selection()
        if not selected:
            self.status_lbl.config(text="Please select a recipe to edit")
            return

        recipe_id = self.tree.item(selected[0])['values'][0]
        recipe = self.db.get_recipe(recipe_id)
        if recipe:
            self.current_recipe = recipe
            self.name_entry.insert(0, recipe.name)
            self.cuisine_cb.set(recipe.cuisine)
            self.prep_sp.delete(0, tk.END)
            self.prep_sp.insert(0, str(recipe.preparation_time))
            self.description_txt.insert('1.0', recipe.description)
            self.ingredients_txt.insert('1.0', recipe.ingredients)
            self.steps_txt.insert('1.0', recipe.instructions)
            self.create_btn.config(text="Update")
            self.status_lbl.config(text=f"Editing recipe: {recipe.name}")

    def _delete_recipe(self):
        selected = self.tree.selection()
        if not selected:
            self.status_lbl.config(text="Please select a recipe to delete")
            return

        recipe_id = self.tree.item(selected[0])['values'][0]
        if self.db.delete_recipe(recipe_id):
            self._load_recipes()
            self._clear_form()
            self.status_lbl.config(text=f"Recipe #{recipe_id} deleted")

    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            recipe_id = self.tree.item(selected[0])['values'][0]
            recipe = self.db.get_recipe(recipe_id)
            if recipe:
                self.status_lbl.config(text=f"Selected recipe: {recipe.name}")

    def run(self) -> None:
        self.app.mainloop()
        
    def __del__(self):
        # Unpack all labels
        pass


# Usage example:
if __name__ == "__main__":
    gui = CulinaryGUI()
    gui.run()