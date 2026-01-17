import tkinter as tk
from tkinter import ttk

class Calculator(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        
        # Header
        self.label = ttk.Label(self, text="Calculus", font=("Segoe UI", 12, "bold"))
        self.label.pack(fill="x", pady=(0, 10))

        # Input fields
        self.inputs_frame = ttk.Frame(self)
        self.inputs_frame.pack(fill="x")

        ttk.Label(self.inputs_frame, text="Page Total (Calculated):", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5, 0))
        self.calc_value = ttk.Entry(self.inputs_frame, font=("Segoe UI", 10))
        self.calc_value.pack(fill="x", pady=(0, 10))

        ttk.Label(self.inputs_frame, text="Verified Value (Manual):").pack(anchor="w", pady=(5, 0))
        self.verify_value = ttk.Entry(self.inputs_frame)
        self.verify_value.pack(fill="x", pady=(0, 10))
        
        # Buttons
        self.btn_frame = ttk.Frame(self)
        self.btn_frame.pack(fill="x", pady=20)

        self.analyze_btn = ttk.Button(self.btn_frame, text="✨ Analyze with AI", style="Accent.TButton", command=self.on_analyze)
        self.analyze_btn.pack(fill="x", pady=5)
        
        self.save_btn = ttk.Button(self.btn_frame, text="Save & Next")
        self.save_btn.pack(fill="x", pady=5)
        
        self.flag_btn = ttk.Button(self.btn_frame, text="Flag for Review")
        self.flag_btn.pack(fill="x", pady=5)

        # AI Results Section
        self.results_frame = ttk.LabelFrame(self, text="Detected Transactions", padding=10)
        self.results_frame.pack(fill="both", expand=True, pady=10)

        self.tree = ttk.Treeview(self.results_frame, columns=("amt", "qty", "sub"), show="headings", height=8)
        self.tree.heading("amt", text="Amount")
        self.tree.heading("qty", text="Quantity")
        self.tree.heading("sub", text="Subtotal")
        self.tree.column("amt", width=80, anchor="e")
        self.tree.column("qty", width=60, anchor="center")
        self.tree.column("sub", width=80, anchor="e")
        self.tree.pack(fill="both", expand=True)
        
        # Summary Label below tree
        self.total_label = ttk.Label(self.results_frame, text="Sum: $0.00", font=("Segoe UI", 10, "bold"), anchor="e")
        self.total_label.pack(fill="x", pady=(5, 0))

    def get_verified_amount(self):
        return self.verify_value.get()

    def populate_results(self, tolls, total):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for t in tolls:
            amt = t.get("amount", 0)
            qty = t.get("quantity", 0)
            sub = amt * qty
            self.tree.insert("", "end", values=(f"${amt:.2f}", qty, f"${sub:.2f}"))
            
        # Update calculated value
        self.calc_value.delete(0, tk.END)
        self.calc_value.insert(0, f"{total:.2f}")
        
        # Update summary label
        self.total_label.config(text=f"Sum: ${total:.2f}")

    def on_analyze(self):
        # Placeholder / Mock
        # This is now overridden by App to call real AI
        pass
