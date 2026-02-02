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
        
        # Configure tags for highlighting
        self.tree.tag_configure("highlight", background="#FFFFCC") # Soft pastel yellow
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Export Setup Section
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=15)
        ttk.Label(self, text="Export Setup", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        self.export_path_label = ttk.Label(self, text="Path: (Current Folder)", font=("Segoe UI", 8), foreground="gray")
        self.export_path_label.pack(anchor="w", pady=(2, 5))
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x")
        
        self.export_btn = ttk.Button(btn_frame, text="Set Export Folder", command=self.select_export_folder)
        self.export_btn.pack(side="left", fill="x", expand=True)
        
        self.status_label = ttk.Label(self, text="", font=("Segoe UI", 8))
        self.status_label.pack(anchor="w", pady=5)
        
        self.current_dir = os.getcwd() # Default
        self.refresh_list()

    def select_export_folder(self):
        from services.data_service import DataService
        config = DataService.load_config()
        initial = config.get("export_folder", self.current_dir)
        
        folder = filedialog.askdirectory(initialdir=initial)
        if folder:
            config["export_folder"] = folder
            DataService.save_config(config)
            self.update_export_ui(folder)

    def update_export_ui(self, folder=None):
        from services.data_service import DataService
        if not folder:
            config = DataService.load_config()
            folder = config.get("export_folder")
            
        if folder:
            self.export_path_label.config(text=f"Path: {os.path.basename(folder)}...")
            # Check for file
            file_path, _ = DataService.get_excel_path()
            if os.path.exists(file_path):
                self.status_label.config(text="✅ Excel exists in folder", foreground="green")
            else:
                self.status_label.config(text="📝 New Excel will be created", foreground="blue")
        else:
            self.export_path_label.config(text="Path: (Project Folder)")
            self.status_label.config(text="")

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

    def toggle_highlight_current(self):
        selection = self.tree.selection()
        if not selection:
            return
            
        item_id = selection[0]
        current_tags = list(self.tree.item(item_id, "tags"))
        
        if "highlight" in current_tags:
            current_tags.remove("highlight")
            is_highlighted = False
        else:
            current_tags.append("highlight")
            is_highlighted = True
            
        self.tree.item(item_id, tags=current_tags)
        return is_highlighted
