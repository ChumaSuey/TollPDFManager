import tkinter as tk
from tkinter import ttk, filedialog
import os
from utils.sort_utils import natural_keys

class PDFList(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        
        # Header Frame
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(header_frame, text="Archive Space", font=("Segoe UI", 12, "bold")).pack(side="left")
        
        # Folder Selection Button
        self.folder_btn = ttk.Button(header_frame, text="📂", width=3, command=self.select_folder)
        self.folder_btn.pack(side="right")

        # Treeview for file list
        self.tree = ttk.Treeview(self, show="tree", selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        self.current_dir = os.getcwd() # Default
        self.refresh_list()

    def select_folder(self):
        folder = filedialog.askdirectory(initialdir=self.current_dir)
        if folder:
            self.current_dir = folder
            self.refresh_list()

    def refresh_list(self):
        # Clear
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            files = [f for f in os.listdir(self.current_dir) if f.lower().endswith(".pdf")]
            files.sort(key=natural_keys)
            
            print(f"Refreshed list from: {self.current_dir}") # Debug
            for f in files:
                full_path = os.path.normpath(os.path.join(self.current_dir, f))
                # values must be a tuple, ensure trailing comma
                self.tree.insert("", "end", text=f, values=(full_path,))
        except Exception as e:
            print(f"Error reading directory: {e}")

    def on_select(self, event):
        # To be bound by the main app controller
        pass

    def toggle_flag_current(self):
        selection = self.tree.selection()
        if not selection:
            return
            
        item_id = selection[0]
        current_text = self.tree.item(item_id, "text")
        
        prefix = "🚩 "
        
        if current_text.startswith(prefix):
            # Unflag
            new_text = current_text[len(prefix):]
            is_flagged = False
        else:
            # Flag
            new_text = prefix + current_text
            is_flagged = True
            
        self.tree.item(item_id, text=new_text)
        return is_flagged
