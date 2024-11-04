import tkinter as tk
from tkinter import ttk
import os

from gui import (create_main_window, create_theme_toggle, create_top_panel, 
                 create_bottom_panel, create_dropdown_frame, create_terminal)
from utils import format_folder_name
from k6_runner import run_k6_test_in_terminal, run_k6_test_and_report
from file_handlers import update_file_dropdown
from stdout_redirect import EmbeddedStdout

# Create main window
root = create_main_window()

# Set the initial theme
# root.tk.call("source", "azure.tcl")
# root.tk.call("set_theme", "light")

# Create theme toggle
create_theme_toggle(root)

# Create panels
top_panel = create_top_panel(root)
bottom_panel = create_bottom_panel(root)

# Create dropdown frame
dropdown_frame = create_dropdown_frame(top_panel)

# Add folder dropdown to the dropdown frame
folder_var = tk.StringVar(root)
folders = [f for f in os.listdir("k6-data") if os.path.isdir(os.path.join("k6-data", f))]
formatted_folders = [(format_folder_name(f), f) for f in folders]
folder_var.set(formatted_folders[0][0] if formatted_folders else "")
folder_dropdown = ttk.OptionMenu(dropdown_frame, folder_var, folder_var.get(), 
                                 *[name for name, _ in formatted_folders], 
                                 command=lambda _: update_file_dropdown(folder_var, file_var, file_dropdown))
folder_dropdown.pack(fill="x", padx=5, pady=(5, 2))

# Add file dropdown to the dropdown frame
file_var = tk.StringVar(root)
file_dropdown = ttk.OptionMenu(dropdown_frame, file_var, "")
file_dropdown.pack(fill="x", padx=5, pady=(2, 5))

# Update file dropdown initially
update_file_dropdown(folder_var, file_var, file_dropdown)

# Create terminal
terminal = create_terminal(bottom_panel)

# Create button frame
button_frame = ttk.Frame(dropdown_frame)
button_frame.pack(fill="x", padx=5, pady=(5, 5))

# Add "Run in Terminal" button
run_terminal_button = ttk.Button(button_frame, text="Run in Terminal", 
                                 command=lambda: run_k6_test_in_terminal(folder_var.get(), file_var.get(), terminal, run_terminal_button, run_report_button))
run_terminal_button.pack(side="left", fill="x", expand=True, padx=(0, 2))

# Add "Run and Report" button
run_report_button = ttk.Button(button_frame, text="Run and Report", 
                               command=lambda: run_k6_test_and_report(folder_var.get(), file_var.get(), terminal, run_terminal_button, run_report_button))
run_report_button.pack(side="left", fill="x", expand=True, padx=(2, 0))

# We don't need to redirect stdout anymore, so remove this line:
# sys.stdout = EmbeddedStdout(terminal)

# Run the app
root.mainloop()