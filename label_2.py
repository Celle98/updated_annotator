import os
from tkinter import (
    Tk,
    Label,
    Button,
    Frame,
    LabelFrame,
    messagebox,
    StringVar,
    Radiobutton,
)
from tkinter.filedialog import askdirectory
from tkinter import ttk

import json
from PIL import Image


hierarchy = [
    {"name": "Foo", "children": [
        {"name": "Bar", "children": [
            {"name": "foo_bar_1"},
            {"name": "foo_bar_2"}
        ]}
    ]}
]


def get_complete_text(tree, item):
    item_text = tree.item(item, "text")
    parent = tree.parent(item)
    if parent:
        item_text = f"{get_complete_text(tree, parent)}/{item_text}"
    return item_text


class Annotator:
    def __init__(self, master):
        self.master = master
        master.title("Annotator Studio")
        master.geometry("800x600")
        self.controls = LabelFrame(master, text="Controls", padx=10, pady=10, bg="white")
        self.controls.pack(padx=15, fill="x")
        self.select_button = Button(
            self.controls,
            text="Select Image",
            command=self.select_image,
            bg="lightgray",
            fg="black",
            font=("Arial", 12),
            relief="raised",
            width=15,
        )
        self.select_button.pack(side="left", padx=5)
        self.back_button = Button(
            self.controls,
            text="Previous",
            command=self.back_image,
            state="disabled",
            bg="lightgray",
            fg="black",
            font=("Arial", 12),
            relief="raised",
            width=10,
        )
        self.back_button.pack(side="left", padx=5)
        self.next_button = Button(
            self.controls,
            text="Next",
            command=self.next_image,
            state="disabled",
            bg="lightgray",
            fg="black",
            font=("Arial", 12),
            relief="raised",
            width=10,
        )
        self.next_button.pack(side="left", padx=5)
        self.annotate_button = Button(
            self.controls,
            text="Annotate",
            command=self.annotate_image,
            state="disabled",
            bg="lightgray",
            fg="black",
            font=("Arial", 12),
            relief="raised",
            width=10,
        )
        self.annotate_button.pack(side="left", padx=5)
        self.save_button = Button(
            self.controls,
            text="Save",
            command=self.save_annotation,
            state="disabled",
            bg="lightgray",
            fg="black",
            font=("Arial", 12),
            relief="raised",
            width=10,
        )
        self.save_button.pack(side="left", padx=5)

        self.image = LabelFrame(master, text="Image", padx=10, pady=10, bg="white")
        self.image.pack(padx=15, fill="x")
        self.inner_frame = Frame(self.image, bg="white")
        self.inner_frame.pack()
        self.image_label = Label(
            self.inner_frame, text="No image selected.", font=("Arial", 12), bg="white"
        )
        self.image_label.pack()

        self.labels = LabelFrame(master, text="Labels", padx=10, pady=10, bg="white")
        self.labels.pack(padx=15, pady=10, fill="x")
        self.var = StringVar()
        self.var.set(None)
        positive_button = Radiobutton(
            self.labels,
            text="Positive",
            variable=self.var,
            value="Positive",
            font=("Arial", 12),
            bg="white",
        )
        negative_button = Radiobutton(
            self.labels,
            text="Negative",
            variable=self.var,
            value="Negative",
            font=("Arial", 12),
            bg="white",
        )

        positive_button.pack(side="left", padx=5)
        negative_button.pack(side="left", padx=5)

        self.flags_label = ttk.Label(master, text="Flags", font=("Arial", 12), background="white")
        self.flags_label.pack()
        self.tree = ttk.Treeview(
            master, show="tree", selectmode="extended", style="Custom.Treeview"
        )

        self.add_node("", hierarchy)

        self.tree.pack(expand=True, fill="both", padx=15, pady=10)

        self.add_flag_button = ttk.Button(
            master,
            text="Add Flag",
            command=self.add_flag,
            style="Custom.TButton",
            width=20,
        )
        self.add_flag_button.pack(pady=10)
    
    def add_node(self, parent, items):
        for item in items:
            item_name = item["name"]
            item_children = item.get("children", [])
            
            self.tree.insert(parent, "end", item_name, text=item_name)
            
            if item_children:
                self.add_node(item_name, item_children)

    def add_flag(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select an item in the tree.")
            return
        
        flag_name = messagebox.askstring("Flag Name", "Enter a name for the flag:")
        if not flag_name:
            messagebox.showinfo("Flag Name Required", "Please enter a name for the flag.")
            return

        for item in selected_items:
            self.tree.insert(item, "end", flag_name, text=flag_name)
