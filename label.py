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


hierarchy = {"Foo": {"Bar": {"foo_bar_1": None, "foo_bar_2": None}}}


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
        self.controls, text="Select Image", command=self.select_image, bg="lightgray", fg="black",
            font=("Arial", 12), relief="raised", width=15
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

        self.flags_label = ttk.Label(master, 
                                     text="Flags", font=("Arial", 12),
                                     background="white")
        self.flags_label.pack()
        self.tree = ttk.Treeview(master, 
                                 show="tree", selectmode="extended",
                                 style="Custom.Treeview")

        # Rest of the code remains unchanged


      def add_node(k, v):
            for i, j in v.items():
                self.tree.insert(k, 1, i, text=i)
                if isinstance(j, dict):
                    add_node(i, j)

        for k, v in hierarchy.items():
            self.tree.insert("", 1, k, text=k)
            add_node(k, v)

        self.tree.pack(expand=True, fill="both")

        self.image_files = []
        self.file_index = 0

    def select_image(self):
        self.directory = askdirectory()
        self.image_files = [
            f
            for f in os.listdir(self.directory)
            if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png")
        ]
        self.file_index = 0
        self.filepath = os.path.join(self.directory, self.image_files[self.file_index])
        self.image_label.config(
            text="Image selected: " + os.path.basename(self.filepath)
        )
        self.next_button.config(state="normal")
        self.annotate_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.var.set(0)
        if len(self.image_files) > 1:
            self.back_button.config(state="normal")

        self.load_annotation()
    
    def load_annotation(self):
        annotations = {}
        try:
            with open("annotations.json", "r", encoding="utf-8") as f:
                annotations = json.load(f)
        except FileNotFoundError:
            pass

        filename = self.image_files[self.file_index]

        if filename in annotations:
            annotation_data = annotations[filename]
            if "labels" in annotation_data:
                labels = annotation_data["labels"]
                if "label" in labels:
                    self.var.set(labels["label"])
            if "flags" in annotation_data:
                flags = annotation_data["flags"]
                for flag in flags:
                    item = self.tree.selection()[0]
                    self.tree.selection_remove(item)
                    self.tree.selection_add(flag)
        else:
            self.var.set(None)
            selected_items = self.tree.selection()
            for item in selected_items:
                self.tree.selection_remove(item)

    def back_image(self):
        if self.file_index == 0:
            messagebox.showinfo("No more images", "This is the first image.")
            self.back_button.config(state="disabled")
            return
        self.file_index -= 1
        self.filepath = os.path.join(self.directory, self.image_files[self.file_index])
        self.image_label.config(text="Image selected: "
                                + os.path.basename(self.filepath))
        self.next_button.config(state="normal")
        self.annotate_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.var.set(0)
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.selection_remove(item)
        self.load_annotation() 
    def annotate_image(self):
        self.save_button.config(state="normal")
        with Image.open(self.filepath) as image:
            image.show()
        self.save_button.config(state="normal")

    def next_image(self):
        self.file_index += 1
        if self.file_index >= len(self.image_files):
            messagebox.showinfo(
                "No more images", "There are no more images in this folder."
            )
            self.next_button.config(state="disabled")
            return
        self.filepath = os.path.join(self.directory, self.image_files[self.file_index])
        self.image_label.config(text="Image selected: "
                                 + os.path.basename(self.filepath))
        self.annotate_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.var.set(0)
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.selection_remove(item)
        self.load_annotation()
    def save_annotation(self):
        annotations = {}
        annotations["labels"] = {}
        annotations["flags"] = {}
        filename = self.image_files[self.file_index]

        flags = []
        selected_items = self.tree.selection()
        for item in selected_items:
            item_text = get_complete_text(self.tree, item)
            flags.append(item_text)

        annotations["flags"] = flags

        if self.var.get() in ["Positive", "Negative"]:
            annotations["labels"]["label"] = self.var.get()
        else:
            messagebox.showerror("Error", "Please select a class before saving.")
            return

        try:
            with open("annotations.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}

        if filename not in data:
            data[filename] = {}
        data[filename].update(annotations)

        with open("annotations.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

        messagebox.showinfo(
            "Annotations Saved!", "Annotations have been saved to the disk."
        )
        self.save_button.config(state="disabled")
    
    def show_image_info(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select an image in the tree.")
            return

        image_name = self.tree.item(selected_items[0], "text")
        messagebox.showinfo("Image Info", f"Selected Image: {image_name}")
    
    def delete_annotation(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select an item to delete.")
            return

        item = selected_items[0]
        self.tree.delete(item)

    def clear_annotations(self):
        self.tree.delete(*self.tree.get_children())
    
    def export_annotations(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select items to export.")
            return

        export_data = []
        for item in selected_items:
            item_text = self.tree.item(item, "text")
            export_data.append(item_text)

        export_filename = "annotations.txt"
        with open(export_filename, "w") as f:
            f.write("\n".join(export_data))

        messagebox.showinfo(
            "Export Successful",
            f"The selected annotations have been exported to {export_filename}.",
        )

root = Tk()
my_gui = Annotator(root)
root.mainloop()
