import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict

def get_file_hash(file_path):
    """Calculate the hash of a file using MD5 algorithm."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicate_files(directory):
    """Find duplicate files within a directory."""
    file_hashes = defaultdict(list)
    duplicate_files = []

    # Recursively traverse the directory
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_hash = get_file_hash(file_path)
            file_hashes[file_hash].append(file_path)

    # Identify duplicate files
    for _, duplicates in file_hashes.items():
        if len(duplicates) > 1:
            duplicate_files.extend(duplicates)

    return duplicate_files

def delete_duplicate_files(files):
    """Delete duplicate files."""
    for file_path in files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")

def browse_directory():
    """Browse and select the directory to scan."""
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(tk.END, directory)

def scan_directory():
    """Scan the selected directory for duplicate files."""
    directory = directory_entry.get()

    if not directory:
        messagebox.showerror("Error", "Please select a directory to scan.")
        return

    duplicate_files = find_duplicate_files(directory)

    if duplicate_files:
        messagebox.showinfo("Duplicate Files Found", f"Duplicate files found: {len(duplicate_files)}")
        result_text.delete("1.0", tk.END)
        for file_path in duplicate_files:
            result_text.insert(tk.END, file_path + "\n")
        result_text.config(state=tk.DISABLED)
        delete_button.config(state=tk.NORMAL)
    else:
        messagebox.showinfo("No Duplicate Files", "No duplicate files found.")

def delete_files():
    """Delete the selected duplicate files."""
    selected_files = result_text.selection_get().split("\n")[:-1]
    delete_confirmation = messagebox.askquestion("Delete Files", "Are you sure you want to delete the selected files?")
    if delete_confirmation == "yes":
        delete_duplicate_files(selected_files)
        messagebox.showinfo("Files Deleted", "Selected files have been deleted.")
        result_text.delete("1.0", tk.END)
        delete_button.config(state=tk.DISABLED)

# Create the main window
window = tk.Tk()
window.title("Duplicate File Finder")

# Create and place widgets
directory_label = tk.Label(window, text="Directory:")
directory_label.pack()

directory_entry = tk.Entry(window, width=50)
directory_entry.pack(side=tk.LEFT, padx=5)

browse_button = tk.Button(window, text="Browse", command=browse_directory)
browse_button.pack(side=tk.LEFT, padx=5)

scan_button = tk.Button(window, text="Scan", command=scan_directory)
scan_button.pack(side=tk.LEFT, padx=5)

result_text = tk.Text(window, height=10, width=70)
result_text.pack(pady=10)

delete_button = tk.Button(window, text="Delete Selected Files", command=delete_files, state=tk.DISABLED)
delete_button.pack()

# Run the main event loop
window.mainloop()
