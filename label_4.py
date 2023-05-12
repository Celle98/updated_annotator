import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from PIL import ImageTk, Image


class Annotator:
    def __init__(self, master):
        self.master = master
        master.title("Annotator Studio")
        master.geometry("800x600")
        master.configure(bg="green")

        self.image_frame = tk.Frame(master, bg="white")
        self.image_frame.pack(padx=15, pady=10)

        self.controls_frame = tk.Frame(master, bg="green")
        self.controls_frame.pack(padx=15, pady=10)

        self.annotation_frame = tk.Frame(master, bg="white")
        self.annotation_frame.pack(padx=15, pady=10)

        self.image_label = None
        self.image_files = []
        self.current_image_index = 0

        self.previous_button = tk.Button(
            self.controls_frame,
            text="Previous",
            command=self.show_previous_image,
            state="disabled",
        )
        self.previous_button.pack(side="left", padx=5)

        self.next_button = tk.Button(
            self.controls_frame,
            text="Next",
            command=self.show_next_image,
            state="disabled",
        )
        self.next_button.pack(side="left", padx=5)

        self.annotate_button = tk.Button(
            self.controls_frame, text="Annotate", command=self.annotate_image
        )
        self.annotate_button.pack(side="left", padx=5)

        self.save_button = tk.Button(
            self.controls_frame,
            text="Save",
            command=self.save_annotation,
            state="disabled",
        )
        self.save_button.pack(side="left", padx=5)

        self.annotation_tree = ttk.Treeview(
            self.annotation_frame,
            columns=("Annotation",),
            show="headings",
            selectmode="browse",
        )
        self.annotation_tree.column("Annotation", width=200)
        self.annotation_tree.heading("Annotation", text="Annotation")
        self.annotation_tree.pack(fill="both", expand=True)

        self.load_image_files()

    def load_image_files(self):
        directory = filedialog.askdirectory()
        if directory:
            self.image_files = [
                f
                for f in os.listdir(directory)
                if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png")
            ]
            self.current_image_index = 0
            if self.image_files:
                self.update_image()
                self.update_navigation_buttons()
            else:
                messagebox.showinfo("No Images", "No images found in the directory.")

    def update_image(self):
        image_path = self.image_files[self.current_image_index]
        self.load_image(image_path)

    def load_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((600, 400), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        if self.image_label:
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        else:
            self.image_label = tk.Label(self.image_frame, image=photo)
            self.image_label.pack()

    def update_navigation_buttons(self):
        total_images = len(self.image_files)
        if total_images > 0:
            if self.current_image_index == 0:
                self.previous_button.config(state="disabled")
            else:
                self.previous_button.config(state="normal")

            if self.current_image_index == total_images - 1:
                self.next_button.config(state="disabled")
            else:
                self.next_button.config(state="normal")

    def show_previous_image(self):
              if self.current_image_index > 0:
            self.current_image_index -= 1
            self.update_image()
            self.update_navigation_buttons()

    def show_next_image(self):
        total_images = len(self.image_files)
        if self.current_image_index < total_images - 1:
            self.current_image_index += 1
            self.update_image()
            self.update_navigation_buttons()

    def annotate_image(self):
        annotation = simpledialog.askstring(
            "Annotate Image",
            "Enter annotation for the image:",
            parent=self.master,
        )
        if annotation:
            self.annotation_tree.insert("", "end", values=(annotation,))
            self.save_button.config(state="normal")

    def save_annotation(self):
        annotation_file = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
        )
        if annotation_file:
            annotations = []
            for item in self.annotation_tree.get_children():
                values = self.annotation_tree.item(item)["values"]
                if values:
                    annotations.append(values[0])

            with open(annotation_file, "w") as f:
                json.dump(annotations, f)

            messagebox.showinfo("Annotation Saved", "Annotation saved successfully.")

    def run(self):
        self.master.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    annotator = Annotator(root)
    annotator.run()

       


