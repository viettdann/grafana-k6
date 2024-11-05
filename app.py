from pathlib import Path
from src.gui_interface import K6RunnerUI
from src import common_utilities

# Xác định project root
PROJECT_ROOT = Path(__file__).resolve().parent

# Truyền PROJECT_ROOT cho common_utilities
common_utilities.set_project_root(PROJECT_ROOT)

ui = K6RunnerUI()
# Create and run the UI
root = ui.root
root.mainloop()