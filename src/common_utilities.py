import os
import re
import tkinter as tk

_PROJECT_ROOT = None

def set_project_root(path):
    global _PROJECT_ROOT
    _PROJECT_ROOT = path

def get_project_root():
    global _PROJECT_ROOT
    if _PROJECT_ROOT is not None:
        return _PROJECT_ROOT
    
    # Fallback: tìm project root bằng cách tìm file requirements.txt
    current_path = os.path.abspath(__file__)
    while not os.path.isfile(os.path.join(current_path, 'requirements.txt')):
        parent = os.path.dirname(current_path)
        if parent == current_path:  # Đã đến thư mục gốc
            raise FileNotFoundError("Could not find the project root directory.")
        current_path = parent
    
    _PROJECT_ROOT = current_path  # Lưu lại để sử dụng cho các lần gọi tiếp theo
    return _PROJECT_ROOT

# Các hàm khác giữ nguyên
def format_folder_name(name):
    return ' '.join(word.capitalize() for word in name.replace('-', ' ').split())

def format_file_name(name):
    name = name[:-3]
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', name)
    return ' '.join(word.capitalize() for word in words)

def get_original_filename(formatted_name, folder):
    folder_path = os.path.join("k6-data", folder.replace(' ', '-').lower())
    for f in os.listdir(folder_path):
        if f.endswith('.js') and format_file_name(f) == formatted_name:
            return f
    return None

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