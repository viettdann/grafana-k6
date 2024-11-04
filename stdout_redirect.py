import tkinter as tk

class EmbeddedStdout:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass