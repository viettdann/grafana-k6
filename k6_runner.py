import subprocess
import threading
import os
import tkinter as tk
from utils import get_original_filename
import platform

def build_k6_command(selected_folder, selected_file):
    original_filename = get_original_filename(selected_file, selected_folder)
    if original_filename:
        category = selected_folder.replace(' ', '-').lower()
        
        # Get the full path to the k6 executable
        current_dir = os.path.dirname(os.path.abspath(__file__))
        k6_path = os.path.join(current_dir, 'bin', 'k6.exe' if platform.system() == "Windows" else 'k6')
        k6_config_file = os.path.join(current_dir, 'k6-data', category, original_filename)
        # Use the full path in the command
        command = f'{k6_path} run {k6_config_file}'
        return command
    return None

def run_k6_test_in_terminal(selected_folder, selected_file, terminal, run_button, run_report_button):
    command = build_k6_command(selected_folder, selected_file)
    if not command:
        terminal.config(state=tk.NORMAL)
        terminal.insert(tk.END, "Error: Could not find the selected test file.\n")
        terminal.config(state=tk.DISABLED)
        return

    terminal.config(state=tk.NORMAL)
    terminal.delete(1.0, tk.END)
    terminal.insert(tk.END, f"Running test: {command}\n\n")
    terminal.config(state=tk.DISABLED)

    def run_command():
        try:
            run_button.config(state=tk.DISABLED)
            run_report_button.config(state=tk.DISABLED)

            if platform.system() == "Windows":
                full_command = f'start cmd /K "{command}"'
            elif platform.system() == "Darwin":
                full_command = f"osascript -e 'tell app \"Terminal\" to do script \"{command}\"'"
            else:
                full_command = f"x-terminal-emulator -e {command}"

            subprocess.Popen(full_command, shell=True)
            
            terminal.config(state=tk.NORMAL)
            terminal.insert(tk.END, f"\nTest started in a new terminal window.\n")
            terminal.config(state=tk.DISABLED)
        except Exception as e:
            terminal.config(state=tk.NORMAL)
            terminal.insert(tk.END, f"\nError running test: {str(e)}\n")
            terminal.config(state=tk.DISABLED)
        finally:
            run_button.config(state=tk.NORMAL)
            run_report_button.config(state=tk.NORMAL)

    threading.Thread(target=run_command).start()

def run_k6_test_and_report(selected_folder, selected_file, terminal, run_button, run_report_button):
    command = build_k6_command(selected_folder, selected_file)
    if not command:
        terminal.config(state=tk.NORMAL)
        terminal.insert(tk.END, "Error: Could not find the selected test file.\n")
        terminal.config(state=tk.DISABLED)
        return

    terminal.config(state=tk.NORMAL)
    terminal.delete(1.0, tk.END)
    terminal.insert(tk.END, f"Running test: {command}\n\n")
    terminal.config(state=tk.DISABLED)

    def run_command():
        try:
            run_button.config(state=tk.DISABLED)
            run_report_button.config(state=tk.DISABLED)

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            for line in iter(process.stdout.readline, ''):
                terminal.config(state=tk.NORMAL)
                terminal.insert(tk.END, line)
                terminal.see(tk.END)
                terminal.config(state=tk.DISABLED)

            process.stdout.close()
            return_code = process.wait()

            terminal.config(state=tk.NORMAL)
            terminal.insert(tk.END, f"\nTest completed with return code: {return_code}\n")
            terminal.config(state=tk.DISABLED)

        except Exception as e:
            terminal.config(state=tk.NORMAL)
            terminal.insert(tk.END, f"\nError running test: {str(e)}\n")
            terminal.config(state=tk.DISABLED)
        finally:
            run_button.config(state=tk.NORMAL)
            run_report_button.config(state=tk.NORMAL)

    threading.Thread(target=run_command).start()