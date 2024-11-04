import os
import re

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