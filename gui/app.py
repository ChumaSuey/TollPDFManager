import tkinter as tk
from tkinter import ttk
from .pdf_list import PDFList
from .pdf_viewer import PDFViewer
from .calculator import Calculator
from .calculator import Calculator
from services.pdf_service import PDFHandler
from services.data_service import DataService
from services.ai_service import TollAnalyzer

class TollManagerApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.pdf_handler = PDFHandler()
        self.ai_service = TollAnalyzer()
        
        # Main horizontal paned window
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, sticky="nsew")

        # Left Pane: PDF List
        self.pdf_list = PDFList(self.paned_window)
        self.paned_window.add(self.pdf_list, weight=1)

        # Center Pane: PDF Viewer
        self.pdf_viewer = PDFViewer(self.paned_window)
        self.paned_window.add(self.pdf_viewer, weight=3)

        # Right Pane: Calculator/Verification
        self.calculator = Calculator(self.paned_window)
        self.paned_window.add(self.calculator, weight=1)
        
        # Bindings
        self.pdf_list.tree.bind("<<TreeviewSelect>>", self.load_pdf)
        self.pdf_viewer.bind("<<PrevPage>>", self.prev_page)
        self.pdf_viewer.bind("<<NextPage>>", self.next_page)
        self.pdf_viewer.bind("<<ZoomChanged>>", self.on_zoom_changed)
        
        # Bind Save Button from Calculator
        self.calculator.save_btn.config(command=self.on_save_next)
        self.calculator.analyze_btn.config(command=self.on_run_analysis)
        
    def load_pdf(self, event):
        selection = self.pdf_list.tree.selection()
        if not selection:
            return
            
        item = self.pdf_list.tree.item(selection[0])
        if item['values']:
            full_path = item['values'][0]
            print(f"Attempting to open: {full_path}") # Debug
            if self.pdf_handler.open_pdf(full_path):
                print("PDF Opened successfully. Showing page...")
                # Reset zoom on new file? Or keep user preference?
                # User usually likes persistence, let's keep current zoom_level
                self.show_current_page()
            else:
                print("Failed to open PDF.")

    def on_zoom_changed(self, event):
        self.show_current_page()

    def show_current_page(self):
        page_idx = self.pdf_handler.current_page_idx
        zoom = self.pdf_viewer.zoom_level
        img = self.pdf_handler.get_page_image(page_idx, zoom=zoom)
        # Pass 1-based index for display
        self.pdf_viewer.display_image(img, page_idx + 1, self.pdf_handler.get_page_count())

    def prev_page(self, event=None):
        if self.pdf_handler.current_page_idx > 0:
            self.pdf_handler.current_page_idx -= 1
            self.show_current_page()
        else:
            # Try to go to previous file
            self.navigate_file(-1)

    def next_page(self, event=None):
        if self.pdf_handler.current_page_idx < self.pdf_handler.get_page_count() - 1:
            self.pdf_handler.current_page_idx += 1
            self.show_current_page()
        else:
            # Try to go to next file
            self.navigate_file(1)
            
    def navigate_file(self, direction):
        """
        Selects and loads the next (+1) or previous (-1) file in the list.
        """
        selection = self.pdf_list.tree.selection()
        if not selection:
            return
            
        current_item = selection[0]
        if direction == 1:
            next_item = self.pdf_list.tree.next(current_item)
            if next_item:
                self.pdf_list.tree.selection_set(next_item)
                # selection_set doesn't verify visibility or trigger virtual events usually?
                # But our binding is on <<TreeviewSelect>>.
                # However, programmatic selection in tkinter often triggers it IF configured right, 
                # but often safer to call load manually or ensure event fires.
                # Let's call load_pdf manually effectively by passing None or mocking event.
                # Or just let the binding handle it? 
                # In Tkinter, selection_set triggers <<TreeviewSelect>>.
                self.pdf_list.tree.see(next_item) # Scroll to it
            else:
                print("End of file list.")
        elif direction == -1:
            prev_item = self.pdf_list.tree.prev(current_item)
            if prev_item:
                self.pdf_list.tree.selection_set(prev_item)
                self.pdf_list.tree.see(prev_item)
            else:
                print("Start of file list.")
            
    def on_save_next(self):
        # 1. Gather Data
        if not self.pdf_handler.path:
            print("No PDF open to save context for.")
            return

        verified_val = self.calculator.get_verified_amount()
        if not verified_val:
            print("No verified value entered.")
            # Optional: Warning messagebox?
            return

        pdf_name = os.path.basename(self.pdf_handler.path)
        page_num = self.pdf_handler.current_page_idx + 1 # 1-based for human readability
        
        data = {
            "PDF Name": pdf_name,
            "Page Number": page_num,
            "Total Amount": verified_val
        }
        
        # 2. Save
        # Use current_dir from pdf_list as save location
        folder = self.pdf_list.current_dir
        success, msg = DataService.save_toll_entry(folder, data)
        
        if success:
            print(msg)
            # 3. Next (Page or File)
            self.next_page()
            # Clear input?
            self.calculator.verify_value.delete(0, tk.END)
            self.calculator.calc_value.delete(0, tk.END)
        else:
            print(f"Save Failed: {msg}")

    def on_run_analysis(self):
        if not self.pdf_handler.path:
            return
            
        print("Running AI Analysis...")
        # Get high-res image for AI (Zoom 2.0)
        page_idx = self.pdf_handler.current_page_idx
        img = self.pdf_handler.get_page_image(page_idx, zoom=2.0)
        
        # Call Service
        # Use threading to prevent UI freeze? For now, sync is okay for prototype.
        result = self.ai_service.analyze_page(img)
        
        # Check error
        if "error" in result:
            print(f"Analysis Error: {result['error']}")
            return

        tolls = result.get("tolls", [])
        total = result.get("total_calculated", 0.0)
        
        # Populate
        self.calculator.populate_results(tolls, total)
        print("Analysis Complete.")
