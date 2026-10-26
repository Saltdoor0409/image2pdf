import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageOps


class ImageToPDFApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Merger & Converter")
        self.root.geometry("540x450")
        self.root.minsize(500, 420)

        # List to store full file paths of selected images
        self.file_paths = []
        self.setup_ui()

    def setup_ui(self):
        # 1. Top button bar (Add Files, Remove Selected, Clear All)
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=8)

        btn_width = 15
        tk.Button(
            top_frame, text="Add Files", width=btn_width, command=self.add_files
        ).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(
            top_frame,
            text="Remove Selected",
            width=btn_width,
            command=self.remove_selected,
        ).pack(side=tk.LEFT, padx=6)
        tk.Button(
            top_frame, text="Clear All", width=btn_width, command=self.clear_all
        ).pack(side=tk.LEFT, padx=6)

        # 2. Center file listbox with vertical scrollbar
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(
            list_frame,
            selectmode=tk.EXTENDED,
            yscrollcommand=scrollbar.set,
            activestyle="none",
        )
        scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 3. Move Up / Move Down buttons and file counter label
        move_frame = tk.Frame(self.root)
        move_frame.pack(fill=tk.X, padx=10, pady=6)

        tk.Button(
            move_frame, text="↑ Move Up", width=12, command=self.move_up
        ).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(
            move_frame, text="↓ Move Down", width=12, command=self.move_down
        ).pack(side=tk.LEFT, padx=6)

        self.count_label = tk.Label(move_frame, text="0 file(s)")
        self.count_label.pack(side=tk.RIGHT)

        # 4. Sorting controls (Sort by criteria and order)
        sort_frame = tk.Frame(self.root)
        sort_frame.pack(fill=tk.X, padx=10, pady=4)

        tk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT, padx=(0, 6))

        self.sort_by_var = tk.StringVar(value="File Name")
        sort_by_combo = ttk.Combobox(
            sort_frame,
            textvariable=self.sort_by_var,
            state="readonly",
            width=14,
            values=["File Name", "Modified Time", "File Size"],
        )
        sort_by_combo.pack(side=tk.LEFT, padx=(0, 6))

        self.sort_order_var = tk.StringVar(value="Ascending")
        sort_order_combo = ttk.Combobox(
            sort_frame,
            textvariable=self.sort_order_var,
            state="readonly",
            width=12,
            values=["Ascending", "Descending"],
        )
        sort_order_combo.pack(side=tk.LEFT, padx=(0, 6))

        tk.Button(sort_frame, text="Sort", width=10, command=self.sort_files).pack(
            side=tk.LEFT
        )

        # 5. Progress bar
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(fill=tk.X, padx=10, pady=6)

        self.progress = ttk.Progressbar(
            progress_frame, orient=tk.HORIZONTAL, mode="determinate"
        )
        self.progress.pack(fill=tk.X, ipady=2)

        # 6. Bottom action button (Merge & Save)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=(2, 10))

        self.convert_btn = tk.Button(
            btn_frame,
            text="Merge PDFs & Save",
            bg="#1a66ff",
            fg="white",
            activebackground="#0052cc",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            height=2,
            command=self.convert_to_pdf,
        )
        self.convert_btn.pack(fill=tk.X)

    def refresh_listbox(self, selected_indices=None):
        # Clear and repopulate the listbox with file names
        self.listbox.delete(0, tk.END)
        for path in self.file_paths:
            self.listbox.insert(tk.END, os.path.basename(path))
        self.count_label.config(text=f"{len(self.file_paths)} file(s)")

        # Restore selection if specified
        if selected_indices:
            for idx in selected_indices:
                if 0 <= idx < len(self.file_paths):
                    self.listbox.selection_set(idx)

    def add_files(self):
        # Open file dialog to select multiple image files
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.bmp *.webp *.tiff *.tif *.gif",
                ),
                ("All Files", "*.*"),
            ],
        )
        if files:
            for f in files:
                self.file_paths.append(f)
            self.refresh_listbox()

    def remove_selected(self):
        # Remove currently selected items in reverse order to avoid index shifting
        selected = list(self.listbox.curselection())
        if not selected:
            return
        for idx in reversed(selected):
            del self.file_paths[idx]
        self.refresh_listbox()

    def clear_all(self):
        # Remove all files and reset the progress bar
        self.file_paths.clear()
        self.refresh_listbox()
        self.progress["value"] = 0

    def move_up(self):
        # Move selected items one position up
        selected = list(self.listbox.curselection())
        if not selected or selected[0] == 0:
            return
        new_selected = []
        for idx in selected:
            self.file_paths[idx - 1], self.file_paths[idx] = (
                self.file_paths[idx],
                self.file_paths[idx - 1],
            )
            new_selected.append(idx - 1)
        self.refresh_listbox(new_selected)

    def move_down(self):
        # Move selected items one position down
        selected = list(self.listbox.curselection())
        if not selected or selected[-1] == len(self.file_paths) - 1:
            return
        new_selected = []
        for idx in reversed(selected):
            self.file_paths[idx + 1], self.file_paths[idx] = (
                self.file_paths[idx],
                self.file_paths[idx + 1],
            )
            new_selected.append(idx + 1)
        self.refresh_listbox(new_selected)

    def sort_files(self):
        # Sort files by name, modified time, or file size
        if not self.file_paths:
            return
        sort_by = self.sort_by_var.get()
        reverse = self.sort_order_var.get() == "Descending"

        if sort_by == "File Name":
            self.file_paths.sort(
                key=lambda x: os.path.basename(x).lower(), reverse=reverse
            )
        elif sort_by == "Modified Time":
            self.file_paths.sort(key=lambda x: os.path.getmtime(x), reverse=reverse)
        elif sort_by == "File Size":
            self.file_paths.sort(key=lambda x: os.path.getsize(x), reverse=reverse)

        self.refresh_listbox()

    def load_image_as_rgb(self, img_path):
        # Load image and apply EXIF orientation
        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)

        # Convert transparent backgrounds (e.g., PNG) to white RGB background
        if img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        ):
            rgba = img.convert("RGBA")
            bg = Image.new("RGB", rgba.size, (255, 255, 255))
            bg.paste(rgba, mask=rgba.split()[3])
            return bg
        return img.convert("RGB")

    def convert_to_pdf(self):
        # Validate file list before conversion
        if not self.file_paths:
            messagebox.showwarning(
                "No Files", "Please add at least one image file first!"
            )
            return

        # Ask user where to save the output PDF
        save_path = filedialog.asksaveasfilename(
            title="Save Merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not save_path:
            return

        processed_images = []
        total = len(self.file_paths)
        self.progress["maximum"] = total
        self.progress["value"] = 0

        try:
            # Process each image and update progress bar
            for idx, path in enumerate(self.file_paths, start=1):
                page_img = self.load_image_as_rgb(path)
                processed_images.append(page_img)
                self.progress["value"] = idx
                self.root.update_idletasks()

            # Save all processed images into a single multi-page PDF
            first_img = processed_images[0]
            rest_imgs = processed_images[1:]
            first_img.save(
                save_path,
                "PDF",
                resolution=300.0,
                save_all=True,
                append_images=rest_imgs,
            )

            messagebox.showinfo(
                "Success", f"PDF created successfully!\nSaved to:\n{save_path}"
            )
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while creating the PDF:\n{str(e)}"
            )
        finally:
            # Close all image objects to free memory
            for im in processed_images:
                im.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToPDFApp(root)
    root.mainloop()