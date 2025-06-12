import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter  # <- import the CustomTkinter module
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
        folder_label.config(text="Output folder selected.")
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
root.configure(bg="#3d3d3d")
root.geometry("450x180")
root.resizable(False, False)

# Styling function for buttons
def style_button(button):
    button.config(font=("Arial", 10), bg="#039dfc", fg="white", activebackground="#0284d4", width=20)

# Grid Layout
tk.Label(root, text="Base Filename", bg="#3d3d3d", fg="white").grid(row=0, column=0, columnspan=1,padx=(10,5), pady=(20, 5), sticky="w")
# base_name_entry = tk.Entry(root, width=30)
base_name_entry = customtkinter.CTkEntry(root, width=180)
base_name_entry.grid(row=0, column=1, columnspan=1, padx=(5,10),pady=(20, 5), sticky="w")

select_tiff_button = customtkinter.CTkButton(root, text="Select TIFF Files",corner_radius=10, command=select_files)
# style_button(select_tiff_button)
select_tiff_button.grid(row=0, column=2, pady=(10,0), sticky="w")

files_label = tk.Label(root, text="No files selected.", fg="white", bg="#3d3d3d")
files_label.grid(row=1, column=2, padx=2, pady=(0,2), sticky="ew")

select_output_button = customtkinter.CTkButton(root, text="Select Output Folder", corner_radius=10, command=select_output_folder)
# style_button(select_output_button)
select_output_button.grid(row=2, column=2, sticky="w")

folder_label = tk.Label(root, text="No folder selected.", fg="white", bg="#3d3d3d")
folder_label.grid(row=3, column=2, padx=20, pady=(0,2), sticky="ew")

convert_button = customtkinter.CTkButton(root, text="Convert", corner_radius=10, command=convert_tiffs_to_pdfs)
# style_button(convert_button)
convert_button.grid(row=4, column=2,sticky="w")

progress_bar = ttk.Progressbar(root, orient="horizontal", length=275, mode="determinate")
progress_bar.grid(row=4, column=0, columnspan=2, pady=2, padx=(10,5), sticky="w")

status_label = tk.Label(root, text="", bg="#3d3d3d")
status_label.grid(row=2, column=0, columnspan=2, padx=20, sticky="w")

root.mainloop()
