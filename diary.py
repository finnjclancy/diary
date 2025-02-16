import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import random
from dotenv import load_dotenv

load_dotenv()
APP_PASSWORD = os.getenv("APP_PASSWORD")

# --- File Paths and Directories ---
GOALS_DIR = "goal_entries"
JOURNAL_DIR = "journal_entries"
DREAM_DIR = "dream_entries"

# Ensure the directories exist
for directory in [GOALS_DIR, JOURNAL_DIR, DREAM_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Global lists to keep track of file names corresponding to listbox entries
goal_files = []
journal_files = []
dream_files = []

# --- Custom Paste Function ---
def custom_paste(event):
    try:
        text = event.widget.clipboard_get()
    except tk.TclError:
        return "break"
    # Remove any unwanted arrow characters (→)
    text = text.replace("→", "")
    event.widget.insert(tk.INSERT, text)
    return "break"

# --- Goals Functions ---
def load_goal_entries():
    """Load all goal entry files from the goals directory into the listbox."""
    goal_files.clear()
    goal_list.delete(0, tk.END)
    files = sorted(os.listdir(GOALS_DIR))
    for file_name in files:
        file_path = os.path.join(GOALS_DIR, file_name)
        try:
            with open(file_path, "r") as f:
                content = f.read().strip()
                summary = content[:50] + ("..." if len(content) > 50 else "")
        except Exception:
            summary = "Error reading file"
        goal_list.insert(tk.END, summary)
        goal_files.append(file_name)

def add_goal():
    """Add a new goal entry using a timestamp as its filename.
    The entry content starts with the timestamp for display."""
    text = goal_entry.get().strip()
    if text:
        dt = datetime.now()
        file_timestamp = dt.strftime("%Y%m%d_%H%M%S")
        display_timestamp = dt.strftime("[%Y-%m-%d %H:%M] ")
        file_name = f"{file_timestamp}.txt"
        file_path = os.path.join(GOALS_DIR, file_name)
        entry_text = display_timestamp + text
        with open(file_path, "w") as f:
            f.write(entry_text)
        load_goal_entries()
        goal_entry.delete(0, tk.END)

def on_goal_double_click(event):
    """Open the selected goal for editing on double-click."""
    selection = goal_list.curselection()
    if selection:
        index = selection[0]
        file_name = goal_files[index]
        file_path = os.path.join(GOALS_DIR, file_name)
        open_goal_editor(file_path, index)

def open_goal_editor(file_path, index):
    """Create an editor window to edit a goal entry."""
    editor = tk.Toplevel(root)
    editor.title("Edit Goal")
    editor.geometry("600x400")
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception:
        content = ""
    text_widget = tk.Text(editor, wrap="word")
    text_widget.insert("1.0", content)
    text_widget.pack(expand=True, fill="both", padx=5, pady=5)
    
    def save_changes():
        new_content = text_widget.get("1.0", tk.END).strip()
        with open(file_path, "w") as f:
            f.write(new_content)
        summary = new_content[:50] + ("..." if len(new_content) > 50 else "")
        goal_list.delete(index)
        goal_list.insert(index, summary)
        editor.destroy()
    
    save_button = ttk.Button(editor, text="Save", command=save_changes)
    save_button.pack(side=tk.LEFT, padx=10, pady=5)
    
    def delete_goal():
        os.remove(file_path)
        goal_list.delete(index)
        del goal_files[index]
        editor.destroy()
    
    delete_button = ttk.Button(editor, text="Delete", command=delete_goal)
    delete_button.pack(side=tk.LEFT, padx=10, pady=5)

# --- Diary (Journal) Functions ---
def load_journal_entries():
    """Load all diary entry files from the journal directory into the listbox."""
    journal_files.clear()
    journal_list.delete(0, tk.END)
    files = sorted(os.listdir(JOURNAL_DIR))
    for file_name in files:
        file_path = os.path.join(JOURNAL_DIR, file_name)
        try:
            with open(file_path, "r") as f:
                content = f.read().strip()
                summary = content[:50] + ("..." if len(content) > 50 else "")
        except Exception:
            summary = "Error reading file"
        journal_list.insert(tk.END, summary)
        journal_files.append(file_name)

def add_journal_entry():
    """Add a new diary entry with the timestamp as its filename.
    The entry content starts with the timestamp for display."""
    text = journal_entry.get("1.0", tk.END).strip()
    if text:
        dt = datetime.now()
        file_timestamp = dt.strftime("%Y%m%d_%H%M%S")
        display_timestamp = dt.strftime("[%Y-%m-%d %H:%M] ")
        file_name = f"{file_timestamp}.txt"
        file_path = os.path.join(JOURNAL_DIR, file_name)
        entry_text = display_timestamp + text
        with open(file_path, "w") as f:
            f.write(entry_text)
        load_journal_entries()
        journal_entry.delete("1.0", tk.END)

def on_journal_entry_double_click(event):
    """Open the selected diary entry for editing on double-click."""
    selection = journal_list.curselection()
    if selection:
        index = selection[0]
        file_name = journal_files[index]
        file_path = os.path.join(JOURNAL_DIR, file_name)
        open_journal_editor(file_path, index)

def open_journal_editor(file_path, index):
    """Create an editor window for a diary entry."""
    editor = tk.Toplevel(root)
    editor.title(f"Editing {os.path.basename(file_path)}")
    editor.geometry("600x400")
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception:
        content = ""
    text_widget = tk.Text(editor, wrap="word")
    text_widget.insert("1.0", content)
    text_widget.pack(expand=True, fill="both", padx=5, pady=5)
    
    def save_changes():
        new_content = text_widget.get("1.0", tk.END).strip()
        with open(file_path, "w") as f:
            f.write(new_content)
        summary = new_content[:50] + ("..." if len(new_content) > 50 else "")
        journal_list.delete(index)
        journal_list.insert(index, summary)
        editor.destroy()
    
    save_button = ttk.Button(editor, text="Save", command=save_changes)
    save_button.pack(side=tk.LEFT, padx=10, pady=5)
    
    def delete_entry():
        try:
            os.remove(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete the file: {e}")
        journal_list.delete(index)
        del journal_files[index]
        editor.destroy()
    
    delete_button = ttk.Button(editor, text="Delete", command=delete_entry)
    delete_button.pack(side=tk.LEFT, padx=10, pady=5)

# --- Dream Functions ---
def load_dream_entries():
    """Load all dream entry files from the dream directory into the listbox."""
    dream_files.clear()
    dream_list.delete(0, tk.END)
    files = sorted(os.listdir(DREAM_DIR))
    for file_name in files:
        file_path = os.path.join(DREAM_DIR, file_name)
        try:
            with open(file_path, "r") as f:
                content = f.read().strip()
                summary = content[:50] + ("..." if len(content) > 50 else "")
        except Exception:
            summary = "Error reading file"
        dream_list.insert(tk.END, summary)
        dream_files.append(file_name)

def add_dream_entry():
    """Add a new dream entry with the timestamp as its filename.
    The entry content starts with the timestamp for display."""
    text = dream_entry.get("1.0", tk.END).strip()
    if text:
        dt = datetime.now()
        file_timestamp = dt.strftime("%Y%m%d_%H%M%S")
        display_timestamp = dt.strftime("[%Y-%m-%d %H:%M] ")
        file_name = f"{file_timestamp}.txt"
        file_path = os.path.join(DREAM_DIR, file_name)
        entry_text = display_timestamp + text
        with open(file_path, "w") as f:
            f.write(entry_text)
        load_dream_entries()
        dream_entry.delete("1.0", tk.END)

def on_dream_entry_double_click(event):
    """Open the selected dream entry for editing on double-click."""
    selection = dream_list.curselection()
    if selection:
        index = selection[0]
        file_name = dream_files[index]
        file_path = os.path.join(DREAM_DIR, file_name)
        open_dream_editor(file_path, index)

def open_dream_editor(file_path, index):
    """Create an editor window for a dream entry."""
    editor = tk.Toplevel(root)
    editor.title(f"Editing {os.path.basename(file_path)}")
    editor.geometry("600x400")
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception:
        content = ""
    text_widget = tk.Text(editor, wrap="word")
    text_widget.insert("1.0", content)
    text_widget.pack(expand=True, fill="both", padx=5, pady=5)
    
    def save_changes():
        new_content = text_widget.get("1.0", tk.END).strip()
        with open(file_path, "w") as f:
            f.write(new_content)
        summary = new_content[:50] + ("..." if len(new_content) > 50 else "")
        dream_list.delete(index)
        dream_list.insert(index, summary)
        editor.destroy()
    
    save_button = ttk.Button(editor, text="Save", command=save_changes)
    save_button.pack(side=tk.LEFT, padx=10, pady=5)
    
    def delete_entry():
        try:
            os.remove(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete the file: {e}")
        dream_list.delete(index)
        del dream_files[index]
        editor.destroy()
    
    delete_button = ttk.Button(editor, text="Delete", command=delete_entry)
    delete_button.pack(side=tk.LEFT, padx=10, pady=5)

# --- Random Entry Function ---
def show_random_entry():
    """Display a random diary or dream entry in a message box."""
    entries = []
    for file_name in journal_files:
        entries.append(os.path.join(JOURNAL_DIR, file_name))
    for file_name in dream_files:
        entries.append(os.path.join(DREAM_DIR, file_name))
    
    if not entries:
        messagebox.showinfo("Random Entry", "No diary or dream entries available.")
        return
    
    random_file = random.choice(entries)
    try:
        with open(random_file, "r") as f:
            content = f.read()
    except Exception:
        content = "Error reading file."
    messagebox.showinfo("Random Entry", content)

# --- Password Login ---
def show_login():
    """Display a login window and verify password before showing the main app."""
    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry("300x150")
    login_window.grab_set()
    
    tk.Label(login_window, text="Enter password:").pack(pady=10)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.pack(pady=5)
    
    def check_password():
        if password_entry.get() == APP_PASSWORD:
            login_window.destroy()
            root.deiconify()
            goal_entry.focus_set()
        else:
            messagebox.showerror("Error", "Incorrect password")
            password_entry.delete(0, tk.END)
    
    ttk.Button(login_window, text="Login", command=check_password).pack(pady=10)
    login_window.protocol("WM_DELETE_WINDOW", root.destroy)

# --- Main Application Window ---
root = tk.Tk()
root.title("Diary")
root.geometry("800x800")

# Set the window icon (requires app_icon.png in the same folder)
try:
    icon = tk.PhotoImage(file="app_icon.png")
    root.iconphoto(True, icon)
except Exception as e:
    print("Icon not found, using default icon.")

# Hide the main window until after login
root.withdraw()

# Force the window to come to the front on launch
root.lift()
root.focus_force()
root.attributes("-topmost", True)
root.after(100, lambda: root.attributes("-topmost", False))

# Override the window close so that it hides (does not quit)
def on_closing():
    root.withdraw()
root.protocol("WM_DELETE_WINDOW", on_closing)

# === Goals Section ===
goal_frame = ttk.LabelFrame(root, text="Goals")
goal_frame.pack(fill="both", expand=True, padx=10, pady=10)

goal_entry = ttk.Entry(goal_frame, width=50)
goal_entry.pack(side=tk.LEFT, padx=5, pady=5)
goal_entry.bind("<Command-v>", custom_paste)
goal_entry.bind("<Control-v>", custom_paste)

add_goal_btn = ttk.Button(goal_frame, text="Add Goal", command=add_goal)
add_goal_btn.pack(side=tk.LEFT, padx=5, pady=5)

goal_list = tk.Listbox(goal_frame, width=80, height=8)
goal_list.pack(fill="both", expand=True, padx=5, pady=5)
goal_list.bind("<Double-Button-1>", on_goal_double_click)

# === Diary Entries Section ===
journal_frame = ttk.LabelFrame(root, text="Diary Entries")
journal_frame.pack(fill="both", expand=True, padx=10, pady=10)

journal_entry = tk.Text(journal_frame, height=3, width=50)
journal_entry.pack(side=tk.LEFT, padx=5, pady=5)
journal_entry.bind("<Command-v>", custom_paste)
journal_entry.bind("<Control-v>", custom_paste)

add_journal_btn = ttk.Button(journal_frame, text="Add Entry", command=add_journal_entry)
add_journal_btn.pack(side=tk.LEFT, padx=5, pady=5)

journal_list = tk.Listbox(journal_frame, width=80, height=8)
journal_list.pack(fill="both", expand=True, padx=5, pady=5)
journal_list.bind("<Double-Button-1>", on_journal_entry_double_click)

# === Dreams Section ===
dream_frame = ttk.LabelFrame(root, text="Dreams")
dream_frame.pack(fill="both", expand=True, padx=10, pady=10)

dream_entry = tk.Text(dream_frame, height=3, width=50)
dream_entry.pack(side=tk.LEFT, padx=5, pady=5)
dream_entry.bind("<Command-v>", custom_paste)
dream_entry.bind("<Control-v>", custom_paste)

add_dream_btn = ttk.Button(dream_frame, text="Add Dream", command=add_dream_entry)
add_dream_btn.pack(side=tk.LEFT, padx=5, pady=5)

dream_list = tk.Listbox(dream_frame, width=80, height=8)
dream_list.pack(fill="both", expand=True, padx=5, pady=5)
dream_list.bind("<Double-Button-1>", on_dream_entry_double_click)

# === Random Entry Section ===
random_entry_btn = ttk.Button(root, text="Show Random Entry", command=show_random_entry)
random_entry_btn.pack(pady=10)

# Load persisted data on startup
load_goal_entries()
load_journal_entries()
load_dream_entries()

# Show the login window first
show_login()

root.mainloop()
