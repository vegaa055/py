import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import img2pdf

# Global state
file_paths = []
output_dir = ""

def select_files():
    global file_paths
    file_paths = filedialog.askopenfilenames(
        title="Select TIFF files",
        filetypes=[("TIFF files", "*.tif *.tiff")]
    )
    if file_paths:
        files_label.config(text=f"{len(file_paths)} file(s) selected.")
    else:
        files_label.config(text="No files selected.")

def select_output_folder():
    global output_dir
    output_dir = filedialog.askdirectory(title="Select Output Folder")
    if output_dir:
        folder_label.config(text=f"Output folder selected.")
    else:
        folder_label.config(text="No folder selected.")

def convert_tiffs_to_pdfs():
    if not file_paths:
        messagebox.showwarning("No Files", "Please select TIFF files first.")
        return
    if not output_dir:
        messagebox.showwarning("No Folder", "Please select an output folder.")
        return

    base_name = base_name_entry.get().strip()
    if not base_name:
        messagebox.showwarning("Missing Filename", "Please enter a base filename.")
        return

    progress_bar['value'] = 0
    status_label.config(text="Starting conversion...")
    root.update_idletasks()

    total = len(file_paths)
    for idx, tiff_path in enumerate(file_paths, start=1):
        try:
            image = Image.open(tiff_path)
            output_filename = f"{base_name}_{idx}.pdf"
            output_path = os.path.join(output_dir, output_filename)

            pdf_bytes = img2pdf.convert(image.filename)
            with open(output_path, "wb") as f:
                f.write(pdf_bytes)

            progress_bar['value'] = (idx / total) * 100
            status_label.config(text=f"Converted: {os.path.basename(tiff_path)}")
            root.update_idletasks()
        except Exception as e:
            print(f"Error converting {tiff_path}: {e}")
            status_label.config(text=f"Error: {os.path.basename(tiff_path)}")

    messagebox.showinfo("Conversion Complete", f"Converted {total} file(s) to PDF.")
    status_label.config(text="Done.")
    progress_bar['value'] = 100

# GUI Setup
root = tk.Tk()
root.title("TIFF to PDF Converter")
root.geometry("400x400")
root.resizable(False, False)

# Widgets
tk.Label(root, text="Base Filename (e.g., invoice, scan):").pack(pady=(20, 5))
base_name_entry = tk.Entry(root, width=30)
base_name_entry.pack()

select_tiff_button = tk.Button(root, text="Select TIFF Files", command=select_files)
select_tiff_button.pack(pady=20, padx=10)
select_tiff_button.config(font=("Arial", 12))
select_tiff_button.config(bg="#4CAF50", fg="white", activebackground="#45a049")

files_label = tk.Label(root, text="No files selected.")
files_label.pack()


select_output_button = tk.Button(root, text="Select Output Folder", command=select_output_folder)
select_output_button.pack(pady=20, padx=10)
select_output_button.config(font=("Arial", 12))
select_output_button.config(bg="#4CAF50", fg="white", activebackground="#45a049")

folder_label = tk.Label(root, text="No folder selected.")
folder_label.pack()

convert_button = tk.Button(root, text="Convert", command=convert_tiffs_to_pdfs)
convert_button.pack(pady=20, padx=10)
convert_button.config(font=("Arial", 12))
convert_button.config(bg="#4CAF50", fg="white", activebackground="#45a049")
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

# Run GUI
root.mainloop()
