import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import img2pdf

def convert_tiffs_to_pdfs(file_paths, output_dir, base_name, progress_bar, status_label):
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
            status_label.config(text=f"Converting: {os.path.basename(tiff_path)}")
            root.update_idletasks()
        except Exception as e:
            print(f"Error converting {tiff_path}: {e}")

    messagebox.showinfo("Conversion Complete", f"Converted {total} file(s) to PDF.")
    status_label.config(text="Done.")
    progress_bar['value'] = 100


def start_conversion():
    file_paths = filedialog.askopenfilenames(
        title="Select TIFF files",
        filetypes=[("TIFF files", "*.tif *.tiff")],
    )
    if not file_paths:
        messagebox.showwarning("No Files", "Please select at least one TIFF file.")
        return

    output_dir = filedialog.askdirectory(title="Select Output Folder")
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

    convert_tiffs_to_pdfs(file_paths, output_dir, base_name, progress_bar, status_label)

# GUI Setup
root = tk.Tk()
root.title("TIFF to PDF Converter")
root.geometry("400x300")
root.resizable(False, False)

# Widgets
tk.Label(root, text="Base Filename (e.g., invoice, scan):").pack(pady=(20, 5))
base_name_entry = tk.Entry(root, width=30)
base_name_entry.pack()

select_button = tk.Button(root, text="Select TIFF Files and Convert", command=start_conversion)
select_button.pack(pady=20, padx=10)
select_button.config(font=("Arial", 12))
select_button.config(bg="#4CAF50", fg="white", activebackground="#45a049")

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

# Run GUI
root.mainloop()
