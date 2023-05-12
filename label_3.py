import os
from tkinter import (
    Tk,
    Label,
    Button,
    Frame,
    LabelFrame,
    StringVar,
    Radiobutton,
)
from tkinter.filedialog import askdirectory
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

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
        master.configure(bg="#e6f2e8")  # Set background color

        self.controls = LabelFrame(
            master,
            text="Controls",
            padx=10,
            pady=10,
            bg="#b3e6cc",  # Set background color
            relief="solid",
            borderwidth=1,
        )
        self.controls.pack(padx=15, fill="x")
        self.select_button = Button(
            self.controls,
            text="Select Image",
            command=self.select_image,
            bg="#70af85",  # Set background color
            fg="white",
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
            bg="#70af85",  # Set background color
            fg="white",
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
            bg="#70af85",  # Set background color
            fg="white",
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
            bg="#70af85",  # Set background color
            fg="white",
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
            bg="#70af85",  # Set background color
            fg="white",
            font=("Arial", 12),
            relief="raised",
            width=10,
        )
        self.save_button.pack(side="left", padx=5)

        self.image = LabelFrame(
            master,
            text="Image",
            padx=10,
            pady=10,
            bg="#b3e6cc",  # Set background color
            relief="solid",
            borderwidth=1,
        )
        self.image.pack(padx=15, fill="x")
       

        self.image_label = Label(self.image)
        self.image_label.pack()

        self.annotations = LabelFrame(
            master,
            text="Annotations",
            padx=10,
            pady=10,
            bg="#b3e6cc",  # Set background color
            relief="solid",
            borderwidth=1,
        )
        self.annotations.pack(padx=15, pady=10, fill="both", expand=True)

        self.annotation_tree = ttk.Treeview(
            self.annotations,
            columns=("Name", "Value"),
            show="headings",
        )
        self.annotation_tree.heading("Name", text="Name")
        self.annotation_tree.heading("Value", text="Value")
        self.annotation_tree.pack(fill="both", expand=True)

        self.select_button.config(state="normal")

    def select_image(self):
        image_dir = askdirectory()
        if image_dir:
            self.image_dir = image_dir
            self.image_files = [
                filename
                for filename in os.listdir(self.image_dir)
                if filename.lower().endswith((".png", ".jpg", ".jpeg"))
            ]
            self.current_image_index = 0

            if self.image_files:
                self.load_image(self.image_files[self.current_image_index])
                self.update_navigation_buttons()
                self.update_annotation_tree()
                self.annotate_button.config(state="normal")
                self.save_button.config(state="normal")
            else:
                self.clear_image()
                self.disable_navigation_buttons()
                self.clear_annotation_tree()
                self.annotate_button.config(state="disabled")
                self.save_button.config(state="disabled")
        else:
            self.clear_image()
            self.disable_navigation_buttons()
            self.clear_annotation_tree()
            self.annotate_button.config(state="disabled")
            self.save_button.config(state="disabled")

    def load_image(self, filename):
        image_path = os.path.join(self.image_dir, filename)
        image = Image.open(image_path)
        image.thumbnail((600, 400))
        self.image_label.config(image=image)
        self.image_label.image = image

    def clear_image(self):
        self.image_label.config(image=None)
        self.image_label.image = None

    def update_navigation_buttons(self):
        if self.current_image_index == 0:
            self.back_button.config(state="disabled")
        else:
            self.back_button.config(state="normal")

        if self.current_image_index == len(self.image_files) - 1:
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")

    def disable_navigation_buttons(self):
        self.back_button.config(state="disabled")
        self.next_button.config(state="disabled")

    def update_annotation_tree(self):
        self.clear_annotation_tree()
        image_filename = self.image_files[self.current_image_index]
        image_name = os.path.splitext(image_filename)[0]
        self.annotation_tree.insert(
            "", "end", values=("Image Name", image_name)
        )

        # Add the hierarchical annotations
        for item in hierarchy:
            self.add_tree_node("", item)

    def clear_annotation_tree(self):
        self.annotation_tree.delete(*self.annotation_tree.get_children())

    def add_tree_node(self, parent, item):
        item_name = item["name"]
        item_children = item.get("children", [])
        self.annotation_tree.insert(parent, "end", values=(item_name, ""))

        for child in item_children:
            self.add_tree_node(item_name, child)

    def back_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image(self.image_files[self.current_image_index])
            self.update_navigation_buttons()
            self.update_annotation_tree()

    def next_image(self):
        if self.current_image_index < len(self.image_files) -1:
            
            self.current_image_index += 1
            self.load_image(self.image_files[self.current_image_index])
            self.update_navigation_buttons()
            self.update_annotation_tree()

    def annotate_image(self):
        selected_item = self.annotation_tree.selection()
        if selected_item:
            complete_text = get_complete_text(self.annotation_tree, selected_item[0])
            new_value = simpledialog.askstring(
                "Annotator Studio", f"Enter value for {complete_text}:"
            )
            if new_value is not None:
                self.annotation_tree.set(selected_item[0], "Value", new_value)

    def save_annotation(self):
        annotations = {}
        for item in self.annotation_tree.get_children():
            self.add_annotation_item(annotations, item)

        save_dir = askdirectory()
        if save_dir:
            image_filename = self.image_files[self.current_image_index]
            annotation_filename = os.path.splitext(image_filename)[0] + ".json"
            annotation_path = os.path.join(save_dir, annotation_filename)
            with open(annotation_path, "w") as file:
                json.dump(annotations, file, indent=4)
            messagebox.showinfo("Annotator Studio", "Annotation saved successfully.")

    def add_annotation_item(self, parent, item):
        item_text = self.annotation_tree.item(item, "text")
        item_value = self.annotation_tree.set(item, "Value")
        if item_text in parent:
            if isinstance(parent[item_text], list):
                parent[item_text].append(item_value)
            else:
                parent[item_text] = [parent[item_text], item_value]
        else:
            parent[item_text] = item_value

        for child in self.annotation_tree.get_children(item):
            self.add_annotation_item(parent[item_text], child)


root = Tk()
annotator = Annotator(root)
root.mainloop()


