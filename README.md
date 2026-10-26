# Image to PDF Merger & Converter

A simple desktop tool built with Python and Tkinter that merges multiple images into a single PDF file. It offers an easy-to-use interface with sorting and reordering, and preserves image quality as much as possible.

---

## ✨ Features

- 📂 **Batch add images**: supports JPG, JPEG, PNG, BMP, WebP, TIFF and GIF
- 🔀 **Reorder freely**: use the "↑ Move Up" and "↓ Move Down" buttons to arrange pages
- 🔃 **Auto sort**: sort by file name, modified time or file size, ascending or descending
- 🗑️ **Remove files**: remove selected files or clear the whole list in one click
- 🖼️ **High-quality output**
  - With `img2pdf` installed: original image data is wrapped directly, giving **fully lossless** results
  - Without it: Pillow is used at maximum quality (quality=100, no chroma subsampling, 300 DPI)
- 🔄 **Automatic EXIF orientation**: photos taken on phones won't end up rotated incorrectly
- ⬜ **Transparency handling**: PNGs with an alpha channel are flattened onto a white background
- 📊 **Progress bar**: shows conversion progress

---

## 📦 Installation

### Requirements

- Python 3.8 or later
- Tkinter (bundled with Python on most systems; some Linux distributions need a separate install)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Install dependencies

Required:

```bash
pip install Pillow
```

Optional (highly recommended for 100% lossless conversion):

```bash
pip install img2pdf
```

> **Linux users**: if tkinter is missing, install it first:
>
> ```bash
> # Debian / Ubuntu
> sudo apt install python3-tk
> # Fedora
> sudo dnf install python3-tkinter
> ```

---

## 🚀 Usage

Run the program:

```bash
python main.py
```


Steps:

1. Click **Add Files** and select one or more images
2. Use **Move Up / Move Down** to reorder, or use **Sort by** to sort automatically
3. Select unwanted images and click **Remove Selected**, or click **Clear All** to empty the list
4. Click **Merge PDFs & Save** and choose where to save the PDF
5. Wait for the progress bar to finish and the success message to appear

---

## 🖥️ Interface Overview

| Area | Description |
| --- | --- |
| Top buttons | Add Files / Remove Selected / Clear All |
| File list | Shows the added images; multi-select is supported |
| Move buttons | Move the selected files up or down; the total file count is shown on the right |
| Sort bar | Choose the sort criterion (File Name / Modified Time / File Size) and order |
| Progress bar | Shows conversion progress |
| Merge PDFs & Save | Starts merging and saves the result as a PDF |

---

## 🔍 Image Quality

| Mode | Condition | Result |
| --- | --- | --- |
| Lossless mode | `img2pdf` installed | Images without transparency or rotation needs are embedded as their original bytes with zero quality loss; images with transparency or rotation are first converted losslessly to PNG |
| High-quality mode | `img2pdf` not installed | Pillow saves with quality=100, subsampling=0 and 300 DPI |

---

## 📁 Export as an EXE File (Optional)

You can package the app into a single `.exe` that runs on Windows without Python installed, using [PyInstaller](https://pyinstaller.org).

> **Note:** PyInstaller does not cross-compile. To get a Windows `.exe`, you must build on Windows.

### Step 1: Install the dependencies

Install everything the app needs, plus PyInstaller. Install `img2pdf` too if you want the lossless mode in the exe.

```bash
pip install Pillow img2pdf pyinstaller
```

### Step 2: Build the executable

Open a terminal in the project folder and run:

```bash
pyinstaller --onefile --windowed --name ImageToPDF main.py
```

| Option | Meaning |
| --- | --- |
| `--onefile` | Bundle everything into a single `.exe` |
| `--windowed` | Hide the console window (GUI app) |
| `--name ImageToPDF` | Name of the output file |

> Replace `main.py` with your actual file name.

### Step 3 (Optional): Add a custom icon

Prepare a `.ico` file and add the `--icon` option:

```bash
pyinstaller --onefile --windowed --name ImageToPDF --icon=icon.ico main.py
```

### Step 4: Find your exe

When the build finishes, the executable is here:

```
dist/ImageToPDF.exe
```

Double-click it to run. You can copy this file to any Windows computer; no Python installation is needed.

### Step 5 (Optional): Clean up build files

PyInstaller also creates a `build/` folder and an `ImageToPDF.spec` file. They are not needed to run the app, and you can add them to `.gitignore`:

```
build/
dist/
*.spec
```

### Step 6 (Optional): Share it on GitHub Releases

1. Go to your repository and click **Releases** → **Draft a new release**
2. Create a tag (for example `v1.0.0`) and add a title
3. Drag `ImageToPDF.exe` into the **Attach binaries** area
4. Click **Publish release**

Users can then download the exe directly without cloning the repository.

### Troubleshooting

- **Antivirus flags the exe**: this is a common false positive with PyInstaller one-file builds. You can build with `--onedir` instead of `--onefile`, or submit the file to your antivirus vendor as a false positive.
- **The exe starts slowly**: one-file builds unpack to a temp folder on each launch. `--onedir` starts faster.
- **"No module named ..." error**: add the missing module with `--hidden-import <module_name>` and rebuild.
- **Build fails with tkinter errors**: reinstall Python from python.org and make sure the "tcl/tk and IDLE" option is selected.

---

## ❓ FAQ

**Q: What size is each PDF page?**
A: Each page takes the pixel dimensions of its image. Images are not scaled or cropped.

**Q: What happens with animated GIFs?**
A: Only the first frame is used.

**Q: I get an error during conversion.**
A: Make sure the image isn't corrupted and that you have write permission for the save location. The error message is shown in a popup.

---

## 🤝 Contributing

Issues and pull requests are welcome!

1. Fork this repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add some feature"`
4. Push the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
