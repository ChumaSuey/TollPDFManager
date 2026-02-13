import unittest
import tkinter as tk
from tkinter import ttk
from gui.calculator import Calculator

class TestInlineEdit(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.calc = Calculator(self.root)
        self.calc.pack()
        
        # Add a test item
        self.calc.tree.insert("", "end", iid="item1", values=("$10.00", 1, "$10.00"))
        self.root.update()

    def tearDown(self):
        self.root.destroy()

    def test_inline_edit_spawn(self):
        # We can't easily simulate a click at x,y without knowing where the item is rendered.
        # But we can call on_double_click with a mock event object IF we knew the coords.
        # Alternatively, we can use the `edit_selected` method which now triggers the inline edit logic for column #1.
        
        # Select item
        self.calc.tree.selection_set("item1")
        
        # Trigger edit
        self.calc.edit_selected()
        
        # Check if entry_popup exists and is mapped
        self.assertTrue(hasattr(self.calc, "entry_popup"))
        self.assertIsNotNone(self.calc.entry_popup)
        self.assertTrue(self.calc.entry_popup.winfo_exists())
        
        # Check value in entry
        self.assertEqual(self.calc.entry_popup.get(), "10.00")

    def test_inline_edit_confirm(self):
        # Trigger edit
        self.calc.tree.selection_set("item1")
        self.calc.edit_selected()
        
        # Change value
        self.calc.entry_popup.delete(0, tk.END)
        self.calc.entry_popup.insert(0, "20.00")
        
        # Confirm (simulate Enter)
        # We need to call on_entry_confirm directly
        self.calc.on_entry_confirm("item1", "#1")
        
        # Verify Tree Updated
        vals = self.calc.tree.item("item1", "values")
        self.assertEqual(vals[0], "$20.00")
        self.assertEqual(vals[2], "$20.00") # Subtotal should update (20 * 1)
        
        # Verify Total Updated
        self.assertEqual(self.calc.total_label.cget("text"), "Sum: $20.00")
        
        # Verify Popup Destroyed
        self.assertIsNone(self.calc.entry_popup)

    def test_inline_edit_cancel(self):
        # Trigger edit
        self.calc.tree.selection_set("item1")
        self.calc.edit_selected()
        
        # Change value but cancel
        self.calc.entry_popup.delete(0, tk.END)
        self.calc.entry_popup.insert(0, "999.00")
        
        # Cancel
        self.calc.on_entry_cancel(None)
        
        # Verify Unchanged
        vals = self.calc.tree.item("item1", "values")
        self.assertEqual(vals[0], "$10.00")

if __name__ == '__main__':
    unittest.main()
