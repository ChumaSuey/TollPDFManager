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

        ttk.Label(
            self.inputs_frame,
            text="Page Total (Calculated):",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(5, 0))
        self.calc_value = ttk.Entry(
            self.inputs_frame, font=("Segoe UI", 10), state="readonly"
        )
        self.calc_value.pack(fill="x", pady=(0, 10))

        ttk.Label(self.inputs_frame, text="Verified Value (Manual):").pack(
            anchor="w", pady=(5, 0)
        )
        self.verify_value = ttk.Entry(self.inputs_frame)
        self.verify_value.pack(fill="x", pady=(0, 10))

        # ... (Buttons skipped for brevity if unchanged, but context requires them)
        # Actually I need to be careful with context matching.
        # I'll just match the init part I need.

        # State for editing
        self.editing_item_id = None

        # ...

        # Buttons
        self.btn_frame = ttk.Frame(self)
        self.btn_frame.pack(fill="x", pady=20)

        self.analyze_btn = ttk.Button(
            self.btn_frame,
            text="✨ Analyze with AI",
            style="Accent.TButton",
            command=self.on_analyze,
        )
        self.analyze_btn.pack(fill="x", pady=5)

        self.save_btn = ttk.Button(self.btn_frame, text="Save & Next")
        self.save_btn.pack(fill="x", pady=5)

        self.flag_btn = ttk.Button(self.btn_frame, text="Flag for Review")
        self.flag_btn.pack(fill="x", pady=5)

        self.highlight_btn = ttk.Button(self.btn_frame, text="📌 Highlight Item")
        self.highlight_btn.pack(fill="x", pady=5)

        # Custom Manual Entry Frame
        self.manual_frame = ttk.LabelFrame(self, text="Manual Entry", padding=10)
        self.manual_frame.pack(fill="x", pady=5)

        # Grid layout for manual inputs
        ttk.Label(self.manual_frame, text="Amount:").grid(
            row=0, column=0, padx=5, sticky="w"
        )
        self.manual_amt = ttk.Entry(self.manual_frame, width=8)
        self.manual_amt.grid(row=0, column=1, padx=5)

        ttk.Label(self.manual_frame, text="Qty:").grid(
            row=0, column=2, padx=5, sticky="w"
        )
        self.manual_qty = ttk.Entry(self.manual_frame, width=5)
        self.manual_qty.insert(0, "1")
        self.manual_qty.grid(row=0, column=3, padx=5)

        self.add_btn = ttk.Button(
            self.manual_frame, text="Add", width=6, command=self.add_manual_entry
        )
        self.add_btn.grid(row=0, column=4, padx=5)

        # AI Results Section
        self.results_frame = ttk.LabelFrame(
            self, text="Detected Transactions", padding=10
        )
        self.results_frame.pack(fill="both", expand=True, pady=10)

        self.tree = ttk.Treeview(
            self.results_frame, columns=("amt", "qty", "sub"), show="headings", height=8
        )
        self.tree.heading("amt", text="Amount")
        self.tree.heading("qty", text="Quantity")
        self.tree.heading("sub", text="Subtotal")
        self.tree.column("amt", width=80, anchor="e")
        self.tree.column("qty", width=60, anchor="center")
        self.tree.column("sub", width=80, anchor="e")
        self.tree.pack(fill="both", expand=True)

        self.total_label = ttk.Label(
            self.results_frame,
            text="Sum: $0.00",
            font=("Segoe UI", 10, "bold"),
            anchor="e",
        )
        self.total_label.pack(fill="x", pady=(5, 0))

        # Editing State
        self.editing_item_id = None

        # List Controls
        ctrl_frame = ttk.Frame(self.results_frame)
        ctrl_frame.pack(fill="x", pady=5)
        ttk.Button(ctrl_frame, text="Edit Selected", command=self.edit_selected).pack(
            side="left", padx=2
        )
        ttk.Button(ctrl_frame, text="Delete Selected", command=self.delete_entry).pack(
            side="right", padx=2
        )
        ttk.Button(ctrl_frame, text="Clear All", command=self.clear_all).pack(
            side="right", padx=2
        )

    def get_verified_amount(self):
        return self.verify_value.get()

    def get_calculated_amount(self):
        return self.calc_value.get()

    def add_manual_entry(self):
        try:
            amt = float(self.manual_amt.get())
            qty = int(self.manual_qty.get())
            sub = amt * qty

            if self.editing_item_id:
                # Update existing
                self.tree.item(
                    self.editing_item_id, values=(f"${amt:.2f}", qty, f"${sub:.2f}")
                )
                self.editing_item_id = None
                self.add_btn.config(text="Add")
            else:
                # Add new
                self.tree.insert("", "end", values=(f"${amt:.2f}", qty, f"${sub:.2f}"))

            self.recalculate()
            # Reset
            self.manual_amt.delete(0, tk.END)
            self.manual_qty.delete(0, tk.END)
            self.manual_qty.insert(0, "1")
        except ValueError:
            pass  # Ignore invalid inputs

    def edit_selected(self):
        selection = self.tree.selection()
        if not selection:
            return

        item_id = selection[0]
        vals = self.tree.item(item_id)["values"]
        # vals: ("$5.50", "2", ...)

        # Parse amount
        amt_str = str(vals[0]).replace("$", "").replace(",", "")
        qty_str = str(vals[1])

        # Load into inputs
        self.manual_amt.delete(0, tk.END)
        self.manual_amt.insert(0, amt_str)

        self.manual_qty.delete(0, tk.END)
        self.manual_qty.insert(0, qty_str)

        # Set state
        self.editing_item_id = item_id
        self.add_btn.config(text="Update")

    def delete_entry(self):
        selection = self.tree.selection()
        if selection:
            for item in selection:
                self.tree.delete(item)
            self.recalculate()

    def clear_all(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.verify_value.delete(0, tk.END)
        self.recalculate()

    def recalculate(self):
        total = 0.0
        for item in self.tree.get_children():
            vals = self.tree.item(item)["values"]
            sub_str = str(vals[2]).replace("$", "").replace(",", "")
            total += float(sub_str)

        # Update UI (Unlock -> Write -> Lock)
        self.calc_value.config(state="normal")
        self.calc_value.delete(0, tk.END)
        self.calc_value.insert(0, f"{total:.2f}")
        self.calc_value.config(state="readonly")

        self.total_label.config(text=f"Sum: ${total:.2f}")

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
        self.calc_value.config(state="normal")
        self.calc_value.delete(0, tk.END)
        self.calc_value.insert(0, f"{total:.2f}")
        self.calc_value.config(state="readonly")

        # Update summary label
        self.total_label.config(text=f"Sum: ${total:.2f}")

    def on_analyze(self):
        pass
