import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

class PDFViewer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        
        # Header
        self.label = ttk.Label(self, text="Center Space (Viewer)", font=("Segoe UI", 12, "bold"))
        self.label.pack(fill="x", pady=(0, 10))

        # Canvas Frame (Scrollable)
        self.canvas_frame = ttk.Frame(self, style="Card.TFrame")
        self.canvas_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Canvas
        self.canvas = tk.Canvas(self.canvas_frame, bg="#2b2b2b", highlightthickness=0)
        self.scrollbar_y = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Placeholder
        self.canvas.create_text(300, 200, text="Select a PDF from Archive Space", fill="white", font=("Segoe UI", 12), tags="placeholder")

        # Navigation Bar
        self.nav_frame = ttk.Frame(self)
        self.nav_frame.pack(fill="x")
        
        self.prev_btn = ttk.Button(self.nav_frame, text="< Prev", command=self.prev_page, state="disabled")
        self.prev_btn.pack(side="left")
        
        self.page_label = ttk.Label(self.nav_frame, text="Page - / -")
        self.page_label.pack(side="left", padx=20)
        
        self.next_btn = ttk.Button(self.nav_frame, text="Next >", command=self.next_page, state="disabled")
        self.next_btn.pack(side="left")

        # Zoom Controls
        ttk.Separator(self.nav_frame, orient="vertical").pack(side="left", padx=10, fill="y")
        
        self.zoom_out_btn = ttk.Button(self.nav_frame, text="🔍-", width=4, command=lambda: self.change_zoom(-0.2))
        self.zoom_out_btn.pack(side="left", padx=2)
        
        self.zoom_label = ttk.Label(self.nav_frame, text="100%", width=6, anchor="center")
        self.zoom_label.pack(side="left", padx=2)
        
        self.zoom_in_btn = ttk.Button(self.nav_frame, text="🔍+", width=4, command=lambda: self.change_zoom(0.2))
        self.zoom_in_btn.pack(side="left", padx=2)

        # State
        self.current_image = None
        self.tk_image = None
        self.zoom_level = 1.0
        
        # Bind Ctrl+Wheel for Zoom (Windows/Linux)
        self.canvas.bind("<Control-MouseWheel>", self.on_ctrl_wheel)
        # Bind also on the frame just in case focus is slightly off, though canvas usually needs focus
        # We'll rely on canvas for now.

    def on_ctrl_wheel(self, event):
        # Windows: event.delta is +/- 120
        if event.delta > 0:
            self.change_zoom(0.2)
        else:
            self.change_zoom(-0.2)

    def change_zoom(self, delta):
        new_zoom = round(self.zoom_level + delta, 1)
        # partial constraint (0.4x to 3.0x)
        if 0.4 <= new_zoom <= 3.0:
            self.zoom_level = new_zoom
            self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
            self.event_generate("<<ZoomChanged>>")

    def display_image(self, pil_image, page_num, total_pages):
        self.canvas.delete("all")
        if not pil_image:
            return

        # Resize logic could go here (fit to width)
        # For now, display as is
        self.tk_image = ImageTk.PhotoImage(pil_image)
        
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.page_label.config(text=f"Page {page_num + 1} / {total_pages}") # page_num is 0-indexed passed as 0, but label wants 1
        # Wait, app.py passes 1-indexed? No wait, app.py passes 1. Let's align. 
        # App.py passed 1. So formatting there.
        # Let's fix app.py to pass 0-indexed or fix display. 
        # Let's assume input 'page_num' is 1-based index for display.
        self.page_label.config(text=f"Page {page_num} / {total_pages}")
        
        # Enable/Disable buttons
        # Smart Navigation: Always enable buttons to allow file switching at boundaries
        self.prev_btn.config(state="normal")
        self.next_btn.config(state="normal")

    def prev_page(self):
        self.event_generate("<<PrevPage>>")

    def next_page(self):
        self.event_generate("<<NextPage>>")
