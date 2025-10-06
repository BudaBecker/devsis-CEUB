import tkinter as tk
from tkinter import ttk

import ttkbootstrap as tb
from ttkbootstrap.constants import *


class CulinaryGUI:
    def __init__(self):
        self.app = tb.Window(themename="superhero")
        self.app.title("Culinary Recipes — CRUD App")
        self.app.iconbitmap('app/img/app_icon.ico')
        self.app.geometry("1200x720")
        self.app.minsize(1000, 600)

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

        # Right: Form
        form = tb.Labelframe(main, text="Recipe Details", padding=12)
        form.grid(row=0, column=1, sticky=NS, padx=(0, 12))
        for i in range(0, 20):
            form.grid_rowconfigure(i, pad=2)
        # Row 0: Name
        tb.Label(form, text="Name").grid(row=0, column=0, sticky=W, pady=(0, 2))
        self.name_entry = tb.Entry(form, width=34)
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky=EW)

        # Row 2: Prep time and Cuisine
        tb.Label(form, text="Cuisine").grid(row=2, column=1, sticky=W, pady=(8, 2))
        self.cuisine_cb = ttk.Combobox(
            form,
            values=["American", "Brazilian", "Italian", "Mexican", "Indian", "Japanese", "Other"],
            state="readonly",
            width=16,
        )
        self.cuisine_cb.grid(row=3, column=1, sticky=EW)
        tb.Label(form, text="Prep Time (min)").grid(row=2, column=0, sticky=W, pady=(8, 2))
        self.prep_sp = ttk.Spinbox(form, from_=0, to=1000, width=10)
        self.prep_sp.grid(row=3, column=0, sticky=EW)

        # Row 3: Description
        tb.Label(form, text="Description").grid(row=4, column=0, sticky=W, pady=(8, 2))
        description_frame = tb.Frame(form)
        description_frame.grid(row=5, column=0, columnspan=2, sticky=EW)
        description_frame.grid_columnconfigure(0, weight=1)
        self.description_txt = tk.Text(description_frame, height=6, wrap="word")
        self.description_txt.grid(row=0, column=0, sticky=EW)
        description_scroll = ttk.Scrollbar(description_frame, orient="vertical", command=self.description_txt.yview)
        description_scroll.grid(row=0, column=1, sticky=NS)
        self.description_txt.configure(yscrollcommand=description_scroll.set)

        # Row 8-11: Ingredients (Text + Scrollbar)
        tb.Label(form, text="Ingredients").grid(row=8, column=0, columnspan=2, sticky=W, pady=(10, 2))
        ingredients_frame = tb.Frame(form)
        ingredients_frame.grid(row=9, column=0, columnspan=2, sticky=EW)
        ingredients_frame.grid_columnconfigure(0, weight=1)
        ingredients_txt = tk.Text(ingredients_frame, height=8, wrap="word")
        ingredients_txt.grid(row=0, column=0, sticky=EW)
        ingredients_scroll = ttk.Scrollbar(ingredients_frame, orient="vertical", command=ingredients_txt.yview)
        ingredients_scroll.grid(row=0, column=1, sticky=NS)
        ingredients_txt.configure(yscrollcommand=ingredients_scroll.set)

        # Row 12-15: Steps (Text + Scrollbar)
        tb.Label(form, text="Steps / Method").grid(row=12, column=0, columnspan=2, sticky=W, pady=(10, 2))
        steps_frame = tb.Frame(form)
        steps_frame.grid(row=13, column=0, columnspan=2, sticky=EW)
        steps_frame.grid_columnconfigure(0, weight=1)
        steps_txt = tk.Text(steps_frame, height=10, wrap="word")
        steps_txt.grid(row=0, column=0, sticky=EW)
        steps_scroll = ttk.Scrollbar(steps_frame, orient="vertical", command=steps_txt.yview)
        steps_scroll.grid(row=0, column=1, sticky=NS)
        steps_txt.configure(yscrollcommand=steps_scroll.set)

        # Action Buttons
        actions = tb.Frame(form, padding=(0, 10, 0, 0))
        actions.grid(row=16, column=0, columnspan=2, sticky=EW)
        actions.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.create_btn = tb.Button(actions, text="Create", bootstyle=SUCCESS)
        self.create_btn.grid(row=0, column=0, padx=4, sticky=EW)

        # Left: Table (Treeview) --------------------------------------------------
        table_frame = tb.Labelframe(main, text="Recipes", padding=12)
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
        export_btn = tb.Button(bottom_actions, text="Edit", bootstyle=SECONDARY)
        duplicate_btn = tb.Button(bottom_actions, text="Delete", bootstyle=SECONDARY)
        export_btn.pack(side=LEFT, padx=(0, 8))
        duplicate_btn.pack(side=LEFT)

    def _create_status_bar(self):
        status = tb.Frame(self.app, padding=(16, 6))
        status.grid(row=3, column=0, sticky=EW)
        self.status_lbl = tb.Label(status, text="Ready • No recipe selected", bootstyle=SECONDARY)
        self.status_lbl.pack(side=LEFT)

    def _setup_event_handlers(self):
        self.create_btn.config(command=self._create_recipe)

    def _create_recipe(self):
        name = self.name_entry.get().strip()
        cuisine = self.cuisine_cb.get().strip()
        prep = self.prep_sp.get().strip()
        description = self.description_txt.get("1.0", "end").strip()
        if not name:
            self.status_lbl.config(text="Name is required")
            return
        next_id = len(self.tree.get_children()) + 1
        display_desc = (description[:200] + "...") if len(description) > 200 else description
        tag = "evenrow" if next_id % 2 == 0 else "oddrow"
        self.tree.insert("", "end", values=(next_id, name, display_desc, cuisine, prep), tags=(tag,))
        self.status_lbl.config(text=f"Added recipe #{next_id}: {name}")

    def run(self) -> None:
        self.app.mainloop()


# Usage example:
if __name__ == "__main__":
    gui = CulinaryGUI()
    gui.run()