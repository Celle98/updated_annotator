import os
import json
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
from tkinter import messagebox, simpledialog
from tkinter.ttk import Treeview

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
            width=15
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

        self.image_frame = LabelFrame(master, text="Image", padx=10, pady=10, bg="white")
        self.image_frame.pack(padx=15, fill="x")

        self.inner_frame = Frame(self.image_frame, bg="white")
        self.inner_frame.pack()

        self.image_label = Label(
            self.inner_frame,
            text="No image selected.",
            font=("Arial", 12),
            bg="white"
        )
        self.image_label.pack()

        self.labels_frame = LabelFrame(master, text="Labels", padx=10, pady=10, bg="white")
        self.labels_frame.pack(padx=15, pady=10, fill="x")

        self.selected_label = StringVar()
                self.labels_treeview = Treeview(self.labels_frame)
        self.labels_treeview.pack(side="left", fill="y")

        self.labels_treeview.heading("#0", text="Labels", anchor="w")
        self.labels_treeview.bind("<<TreeviewSelect>>", self.select_label)

        self.labels_scrollbar = LabelFrame(self.labels_frame, bg="white")
        self.labels_scrollbar.pack(side="left", fill="y")

        self.scrollbar = Scrollbar(self.labels_scrollbar, orient="vertical", command=self.labels_treeview.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.labels_treeview.configure(yscrollcommand=self.scrollbar.set)

        self.flags_frame = LabelFrame(master, text="Flags", padx=10, pady=10, bg="white")
        self.flags_frame.pack(padx=15, pady=10, fill="x")

        self.flags_treeview = Treeview(self.flags_frame)
        self.flags_treeview.pack(side="left", fill="y")

        self.flags_treeview.heading("#0", text="Flags", anchor="w")
        self.flags_treeview.bind("<<TreeviewSelect>>", self.select_flag)

        self.flags_scrollbar = LabelFrame(self.flags_frame, bg="white")
        self.flags_scrollbar.pack(side="left", fill="y")

        self.scrollbar = Scrollbar(self.flags_scrollbar, orient="vertical", command=self.flags_treeview.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.flags_treeview.configure(yscrollcommand=self.scrollbar.set)

        self.image_index = 0
        self.image_files = []
        self.current_image = None
        self.current_annotation = {}

        self.load_hierarchy(hierarchy)

    def load_hierarchy(self, hierarchy):
        self.labels_treeview.delete(*self.labels_treeview.get_children())
        self.flags_treeview.delete(*self.flags_treeview.get_children())

        for item in hierarchy:
            self.insert_label_item("", item)

    def insert_label_item(self, parent, item):
        item_name = item["name"]
        self.labels_treeview.insert(parent, "end", text=item_name)

        if "children" in item:
            for child in item["children"]:
                self.insert_label_item(item_name, child)

    def select_label(self, event):
        selected_item = self.labels_treeview.focus()
        label_text = self.labels_treeview.item(selected_item, "text")
        self.selected_label.set(label_text)

    def select_flag(self, event):
        selected_item = self.flags_treeview.focus()
        flag_text = self.flags_treeview.item(selected_item, "text")
        self.selected_flag.set(flag_text)

    def select_image(self):
        directory = askdirectory()
        if directory:
            self.image_files = [f for f in os.listdir(directory) if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png")]
            if self.image_files:
                self.image_index = 0
                self.load_image()

    def load_image(self):
        image_path = self.image_files[self.image_index]
        self.current_image = Image.open(image_path)
        self.current_annotation = {"image_path": image_path, "labels": [], "flags": []}
        self.show_image()

    def show_image(self):
        self.image_label.configure(image=self.current_image)
        self.image_label.image = self.current_image

        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        num_images = len(self.image_files)

        self.back_button.configure(state="normal" if self.image_index > 0 else "disabled")
                self.next_button.configure(state="normal" if self.image_index < num_images - 1 else "disabled")
        self.annotate_button.configure(state="normal")
        self.save_button.configure(state="normal")

    def back_image(self):
        if self.image_index > 0:
            self.image_index -= 1
            self.load_image()

    def next_image(self):
        num_images = len(self.image_files)
        if self.image_index < num_images - 1:
            self.image_index += 1
            self.load_image()

    def annotate_image(self):
        if self.current_image is not None:
            selected_label = self.selected_label.get()
            selected_flag = self.selected_flag.get()

            if selected_label and selected_flag:
                self.current_annotation["labels"].append(selected_label)
                self.current_annotation["flags"].append(selected_flag)
                self.next_image()

            else:
                messagebox.showwarning("Incomplete Annotation", "Please select a label and a flag before annotating.")

    def save_annotation(self):
        annotation_file = simpledialog.askstring("Save Annotation", "Enter the annotation file name:")
        if annotation_file:
            with open(annotation_file, "w") as f:
                json.dump(self.current_annotation, f)
            messagebox.showinfo("Annotation Saved", "Annotation file saved successfully.")

    def run(self):
        self.master.mainloop()


if __name__ == "__main__":
    root = Tk()
    annotator = Annotator(root)
    annotator.run()


       
