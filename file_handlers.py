import os
import tkinter as tk
from utils import format_file_name, format_folder_name

def update_file_dropdown(folder_var, file_var, file_dropdown):
    selected_folder = folder_var.get()
    file_dropdown['menu'].delete(0, 'end')

    folder_path = os.path.join("k6-data", selected_folder.replace(' ', '-').lower())
    if os.path.exists(folder_path):
        js_files = [f for f in os.listdir(folder_path) if f.endswith('.js')]
        formatted_files = [(format_file_name(f), f) for f in js_files]
        for formatted_name, original_name in formatted_files:
            file_dropdown['menu'].add_command(label=formatted_name, 
                                              command=tk._setit(file_var, formatted_name))
        if formatted_files:
            file_var.set(formatted_files[0][0])
        else:
            file_var.set("")