import tkinter as tk
from tkinter import ttk

import ttkbootstrap as tb
from ttkbootstrap.constants import *

class RecipeList(tb.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
    
    # Left: Table (Treeview) --------------------------------------------------
        table_frame = tb.Labelframe(parent, text="Recipes", padding=12)
        table_frame.grid(row=0, column=0, sticky=NSEW)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        columns = ("id", "name", "description", "cuisine", "prep")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=18,
        )
        self.tree.grid(row=0, column=0, sticky=NSEW)

        # Headings
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("description", text="Description")
        self.tree.heading("cuisine", text="Cuisine")
        self.tree.heading("prep", text="Prep (min)")

        # Column widths (fixed)
        self.tree.column("id", width=40, anchor=W, stretch=False)
        self.tree.column("name", width=160, anchor=W, stretch=False)
        self.tree.column("description", width=420, anchor=W, stretch=False)
        self.tree.column("cuisine", width=120, anchor=W, stretch=False)
        self.tree.column("prep", width=80, anchor=W, stretch=False)

        # Style the Treeview for table look
        self.style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.tree.tag_configure("oddrow", background=self.style.colors.bg, foreground=self.style.colors.fg)
        self.tree.tag_configure("evenrow", background="#f3f6f9")  # subtle stripe

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        y_scroll.grid(row=0, column=1, sticky=NS)
        x_scroll.grid(row=1, column=0, sticky=EW)

        # Bottom action row
        bottom_actions = tb.Frame(table_frame, padding=(0, 8, 0, 0))
        bottom_actions.grid(row=2, column=0, columnspan=2, sticky=EW)
        self.edit_btn = tb.Button(bottom_actions, text="Edit", bootstyle=SECONDARY, command=self._edit_recipe)
        self.delete_btn = tb.Button(bottom_actions, text="Delete", bootstyle=DANGER, command=self._delete_recipe)
        self.edit_btn.pack(side=LEFT, padx=(0, 8))
        self.delete_btn.pack(side=LEFT)

        # Load existing recipes
        self._load_recipes()