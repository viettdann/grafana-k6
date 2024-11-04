import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import sv_ttk
import darkdetect

def create_main_window():
    root = tk.Tk()
    root.title("Grafana K6 Test Runner")
    root.geometry("800x600")
    sv_ttk.set_theme(darkdetect.theme())
    return root

def create_theme_toggle(root):
    theme_frame = ttk.Frame(root)
    theme_frame.pack(fill="x", padx=10, pady=5)

    def change_theme():
        if sv_ttk.get_theme() == "dark":
            sv_ttk.set_theme("light")
            theme_button.configure(text="🌙 Dark Mode")
        else:
            sv_ttk.set_theme("dark")
            theme_button.configure(text="☀️ Light Mode")

    theme_button = ttk.Button(
        theme_frame, 
        text="🌙 Dark Mode" if sv_ttk.get_theme() == "light" else "☀️ Light Mode",
        command=change_theme
    )
    theme_button.pack(side="left")

def create_top_panel(root):
    top_panel = ttk.Frame(root, height=300)
    top_panel.pack(side="top", fill="both", expand=True)
    top_panel.pack_propagate(False)
    
    top_title = ttk.Label(top_panel, text="Grafana K6", font=("TkDefaultFont", 16, "bold"))
    top_title.pack(pady=(10, 20))
    
    return top_panel

def create_bottom_panel(root):
    bottom_panel = ttk.Frame(root, height=300)
    bottom_panel.pack(side="bottom", fill="both", expand=True)
    bottom_panel.pack_propagate(False)
    
    bottom_title = ttk.Label(bottom_panel, text="Results", font=("TkDefaultFont", 16, "bold"))
    bottom_title.pack(pady=(10, 20))
    
    return bottom_panel

def create_dropdown_frame(top_panel):
    dropdown_frame = ttk.LabelFrame(top_panel, text="Categories and Tests", padding=(10, 5))
    dropdown_frame.pack(fill="x", expand=False, padx=10, pady=10)
    return dropdown_frame

def create_terminal(bottom_panel):
    terminal_frame = ttk.Frame(bottom_panel)
    terminal_frame.pack(fill="both", expand=True, padx=10, pady=10)

    terminal = scrolledtext.ScrolledText(terminal_frame, wrap=tk.WORD, bg='black', fg='white')
    terminal.pack(fill="both", expand=True)
    terminal.insert(tk.END, "Terminal ready. Run a test to see results.\n")
    terminal.config(state=tk.DISABLED)
    
    return terminal