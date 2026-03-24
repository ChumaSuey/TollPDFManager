import os
from tkinter import filedialog, ttk

from utils.sort_utils import natural_keys


class PDFList(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)

        # Header Frame
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(
            header_frame, text="Archive Space", font=("Segoe UI", 12, "bold")
        ).pack(side="left")

        # Folder Selection Button
        self.folder_btn = ttk.Button(
            header_frame, text="📂", width=3, command=self.select_folder
        )
        self.folder_btn.pack(side="right")

        # Treeview for file list
        self.tree = ttk.Treeview(self, show="tree", selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Configure tags for highlighting
        self.tree.tag_configure("highlight", background="#FFFFCC")  # Soft pastel yellow
        # Configure tag for processed files
        self.tree.tag_configure("processed", foreground="green")  # Green text for processed

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Export Setup Section
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=15)
        ttk.Label(self, text="Export Setup", font=("Segoe UI", 10, "bold")).pack(
            anchor="w"
        )

        self.export_path_label = ttk.Label(
            self, text="Path: (Current Folder)", font=("Segoe UI", 8), foreground="gray"
        )
        self.export_path_label.pack(anchor="w", pady=(2, 5))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x")

        self.export_btn = ttk.Button(
            btn_frame, text="Set Export Folder", command=self.select_export_folder
        )
        self.export_btn.pack(side="left", fill="x", expand=True)

        self.status_label = ttk.Label(self, text="", font=("Segoe UI", 8))
        self.status_label.pack(anchor="w", pady=5)

        self.current_dir = os.getcwd()  # Default
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
            # Refresh list to update processed status based on new excel location
            self.refresh_list()

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
                self.status_label.config(
                    text="✅ Excel exists in folder", foreground="green"
                )
            else:
                self.status_label.config(
                    text="📝 New Excel will be created", foreground="blue"
                )
        else:
            self.export_path_label.config(text="Path: (Project Folder)")
            self.status_label.config(text="")

    def select_folder(self):
        folder = filedialog.askdirectory(initialdir=self.current_dir)
        if folder:
            self.current_dir = folder
            self.refresh_list()

    def refresh_list(self):
        from services.data_service import DataService

        # Clear
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            processed_files = DataService.get_processed_tolls(self.current_dir)
        except Exception:
            processed_files = set()

        try:
            # Load persistent flags
            flagged_paths = DataService.load_flags()
        except Exception:
            flagged_paths = set()

        try:
            files = [
                f for f in os.listdir(self.current_dir) if f.lower().endswith(".pdf")
            ]
            files.sort(key=natural_keys)

            print(f"Refreshed list from: {self.current_dir}")  # Debug
            for f in files:
                full_path = os.path.normpath(os.path.join(self.current_dir, f))
                
                tags = []
                display_text = f
                
                # Check processed
                if f in processed_files:
                    tags.append("processed")
                    display_text = "✅ " + display_text
                
                # Check flagged (using full path)
                if full_path in flagged_paths:
                    display_text = "🚩 " + display_text
                    # Ensure flag comes after checkmark if both exist?
                    # If previously "✅ file", now "🚩 ✅ file"?
                    # Or "✅ 🚩 file"? Use consistent order.
                    # My logic above puts it straight.
                    # If processed was processed: "✅ file"
                    # If flag added: "🚩 ✅ file" which is fine.

                # values must be a tuple, ensure trailing comma
                self.tree.insert("", "end", text=display_text, values=(full_path,), tags=tags)
        except Exception as e:
            print(f"Error reading directory: {e}")

    def mark_as_processed(self, filename):
        """
        Updates the visual status of a file to 'processed' without reloading the whole list.
        """
        target_path = os.path.normpath(os.path.join(self.current_dir, filename))
        
        for child in self.tree.get_children():
            item_vals = self.tree.item(child, "values")
            if item_vals and item_vals[0] == target_path:
                current_text = self.tree.item(child, "text")
                current_tags = list(self.tree.item(child, "tags"))
                
                if "processed" not in current_tags:
                    current_tags.append("processed")
                    if not "✅" in current_text:
                        # Find where to insert checkmark
                        # If startswith 🚩, insert after? Or before?
                        # Let's say: "✅ 🚩 file.pdf" is cleanest.
                        if "🚩 " in current_text:
                             # "🚩 file" -> "✅ 🚩 file"
                             new_text = "✅ " + current_text
                        else:
                             new_text = "✅ " + current_text
                        
                        self.tree.item(child, text=new_text, tags=current_tags)
                    else:
                        self.tree.item(child, tags=current_tags)
                return

    def unmark_as_processed(self, filename):
        """
        Removes the 'processed' visual mark from a file if it has no remaining
        entries in the Excel. Checks the Excel first before unmarking.
        """
        from services.data_service import DataService

        # Check if ANY entries remain for this PDF
        remaining = DataService.get_processed_tolls(self.current_dir)

        if filename in remaining:
            # Other pages from this PDF still exist, keep the mark
            return

        target_path = os.path.normpath(os.path.join(self.current_dir, filename))

        for child in self.tree.get_children():
            item_vals = self.tree.item(child, "values")
            if item_vals and item_vals[0] == target_path:
                current_text = self.tree.item(child, "text")
                current_tags = list(self.tree.item(child, "tags"))

                if "processed" in current_tags:
                    current_tags.remove("processed")
                    new_text = current_text.replace("✅ ", "", 1)
                    self.tree.item(child, text=new_text, tags=current_tags)
                return

    def on_select(self, event):
        # To be bound by the main app controller
        pass

    def toggle_flag_current(self):
        from services.data_service import DataService

        selection = self.tree.selection()
        if not selection:
            return

        item_id = selection[0]
        current_text = self.tree.item(item_id, "text")
        full_path = self.tree.item(item_id, "values")[0]

        # Load current flags
        flagged_paths = DataService.load_flags()

        prefix = "🚩 "
        is_flagged = False

        if "🚩 " in current_text:
            # Unflag
            new_text = current_text.replace("🚩 ", "", 1)
            flagged_paths.discard(full_path)
            is_flagged = False
        else:
            # Flag
            # Insert 🚩. If starts with ✅, insert after.
            if current_text.strip().startswith("✅"):
                 # "✅ file" -> "✅ 🚩 file"
                 # Find index of first char after check
                 new_text = current_text.replace("✅ ", "✅ 🚩 ", 1)
            else:
                 new_text = prefix + current_text
            
            flagged_paths.add(full_path)
            is_flagged = True

        # Save persistence
        DataService.save_flags(flagged_paths)
        
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
