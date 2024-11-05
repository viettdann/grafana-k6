import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import sv_ttk
import darkdetect
import os
from src.k6_executor import run_k6_in_terminal, run_k6_and_report
from src.common_utilities import format_folder_name, update_file_dropdown

class K6RunnerUI:
    def __init__(self):
        self.root = self.create_main_window()
        self.create_theme_toggle()
        self.create_panels()
        self.create_dropdowns()
        self.create_terminal()
        self.create_buttons()

    def create_main_window(self):
        root = tk.Tk()
        root.title("Grafana K6 Test Runner")
        root.geometry("800x600")
        sv_ttk.set_theme(darkdetect.theme())
        return root

    def create_theme_toggle(self):
        theme_frame = ttk.Frame(self.root)
        theme_frame.pack(fill="x", padx=10, pady=5)

        self.theme_button = ttk.Button(
            theme_frame, 
            text="🌙 Dark Mode" if sv_ttk.get_theme() == "light" else "☀️ Light Mode",
            command=self.change_theme
        )
        self.theme_button.pack(side="left")

    def change_theme(self):
        if sv_ttk.get_theme() == "dark":
            sv_ttk.set_theme("light")
            self.theme_button.configure(text="🌙 Dark Mode")
        else:
            sv_ttk.set_theme("dark")
            self.theme_button.configure(text="☀️ Light Mode")

    def create_panels(self):
        self.top_panel = self.create_panel("top", "Grafana K6")
        self.bottom_panel = self.create_panel("bottom", "Results")

    def create_panel(self, side, title):
        panel = ttk.Frame(self.root, height=300)
        panel.pack(side=side, fill="both", expand=True)
        panel.pack_propagate(False)
        
        panel_title = ttk.Label(panel, text=title, font=("TkDefaultFont", 16, "bold"))
        panel_title.pack(pady=(10, 20))
        
        return panel

    def create_dropdowns(self):
        dropdown_frame = ttk.LabelFrame(self.top_panel, text="Categories and Tests", padding=(10, 5))
        dropdown_frame.pack(fill="x", expand=False, padx=10, pady=10)

        self.folder_var, self.folder_dropdown = self.create_folder_dropdown(dropdown_frame)
        self.file_var, self.file_dropdown = self.create_file_dropdown(dropdown_frame)

        update_file_dropdown(self.folder_var, self.file_var, self.file_dropdown)

    def create_folder_dropdown(self, parent):
        folder_var = tk.StringVar(self.root)
        folders = [f for f in os.listdir("k6-data") if os.path.isdir(os.path.join("k6-data", f))]
        formatted_folders = [(format_folder_name(f), f) for f in folders]
        folder_var.set(formatted_folders[0][0] if formatted_folders else "")
        
        folder_dropdown = ttk.OptionMenu(
            parent, 
            folder_var, 
            folder_var.get(), 
            *[name for name, _ in formatted_folders], 
            command=lambda _: update_file_dropdown(folder_var, self.file_var, self.file_dropdown)
        )
        folder_dropdown.pack(fill="x", padx=5, pady=(5, 2))
        
        return folder_var, folder_dropdown

    def create_file_dropdown(self, parent):
        file_var = tk.StringVar(self.root)
        file_dropdown = ttk.OptionMenu(parent, file_var, "")
        file_dropdown.pack(fill="x", padx=5, pady=(2, 5))
        return file_var, file_dropdown

    def create_terminal(self):
        terminal_frame = ttk.Frame(self.bottom_panel)
        terminal_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.terminal = scrolledtext.ScrolledText(terminal_frame, wrap=tk.WORD, bg='black', fg='white')
        self.terminal.pack(fill="both", expand=True)
        self.terminal.insert(tk.END, "Terminal ready. Run a test to see results.\n")
        self.terminal.config(state=tk.DISABLED)

    def create_buttons(self):
        button_frame = ttk.Frame(self.top_panel)
        button_frame.pack(fill="x", padx=15, pady=(5, 15))

        self.run_terminal_button = self.create_button(
            button_frame, "Run in Terminal", self.run_in_terminal, side="left"
        )
        self.run_report_button = self.create_button(
            button_frame, "Run and Report", self.run_and_report, side="right"
        )

    def create_button(self, parent, text, command, side):
        button = ttk.Button(parent, text=text, command=command)
        button.pack(side=side, fill="x", expand=True, padx=5)
        return button

    def run_in_terminal(self):
        run_k6_in_terminal(
            self.folder_var.get(), 
            self.file_var.get(), 
            self.terminal, 
            self.run_terminal_button, 
            self.run_report_button
        )

    def run_and_report(self):
        run_k6_and_report(
            self.folder_var.get(), 
            self.file_var.get(), 
            self.terminal, 
            self.run_terminal_button, 
            self.run_report_button
        )