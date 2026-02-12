import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import MagicMock, patch

# Import the Calculator class. 
# We need to mock the parent and services not present in test env
import sys
import os

# Adjust path to find modules
sys.path.append(os.getcwd())

from gui.calculator import Calculator

class TestCalculatorShortcuts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize Tkinter root for widgets (headless)
        cls.root = tk.Tk()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def setUp(self):
        self.calc = Calculator(self.root)
        
        # Mocking external calls in Calculator if any
        # Calculator uses list_models from services.ai_service
        # We assume that import works or doesn't crash 
        # (it was imported in file, hopefully env has it or we cope)

    def tearDown(self):
        self.calc.destroy()

    def test_return_pressed(self):
        # Setup inputs
        self.calc.manual_amt.insert(0, "10.0")
        self.calc.manual_qty.delete(0, tk.END)
        self.calc.manual_qty.insert(0, "2")
        
        # Call handler directly (simulating event)
        self.calc.on_return_pressed(None)
        
        # Check if added to tree
        children = self.calc.tree.get_children()
        self.assertEqual(len(children), 1)
        vals = self.calc.tree.item(children[0])['values']
        # values are strings like "$10.00", 2, "$20.00"
        # Note: treeview values are sometimes returned as strings or actual types depending on version/config
        # Based on code: values=(f"${amt:.2f}", qty, f"${sub:.2f}")
        self.assertEqual(vals[0], "$10.00")
        self.assertEqual(str(vals[1]), "2")
        self.assertEqual(vals[2], "$20.00")
        
        # Check if inputs cleared
        self.assertEqual(self.calc.manual_amt.get(), "")
        self.assertEqual(self.calc.manual_qty.get(), "1")

    def test_escape_pressed(self):
        # Setup inputs
        self.calc.manual_amt.insert(0, "50.0")
        
        # Simulate Enter to add it first (to test clearing edit mode later maybe?)
        # Let's just test clearing inputs
        self.calc.on_escape_pressed(None)
        
        self.assertEqual(self.calc.manual_amt.get(), "")
        self.assertEqual(self.calc.manual_qty.get(), "1")

    def test_double_click_edit(self):
        # Add item
        self.calc.tree.insert("", "end", iid="item1", values=("$5.00", 1, "$5.00"))
        
        # Mock identify_row to return our item
        self.calc.tree.identify_row = MagicMock(return_value="item1")
        
        # Mock editing methods to verify call flow
        # Actually better to verify state
        
        # simulate double click event
        event = MagicMock()
        event.y = 10
        self.calc.on_double_click(event)
        
        # Check if inputs populated
        self.assertEqual(self.calc.manual_amt.get(), "5.00")
        self.assertEqual(self.calc.manual_qty.get(), "1")
        
        # Check if edit mode active
        self.assertEqual(self.calc.editing_item_id, "item1")
        self.assertEqual(self.calc.add_btn.cget("text"), "Update")

    def test_escape_exit_edit_mode(self):
        # Enter edit mode
        self.calc.editing_item_id = "some_id"
        self.calc.add_btn.config(text="Update")
        self.calc.manual_amt.insert(0, "10")
        
        # Press Escape
        self.calc.on_escape_pressed(None)
        
        # Check reset
        self.assertIsNone(self.calc.editing_item_id)
        self.assertEqual(self.calc.add_btn.cget("text"), "Add")
        self.assertEqual(self.calc.manual_amt.get(), "")

    def test_delete_key(self):
        # Add item
        self.calc.tree.insert("", "end", iid="item_del", values=("$10.00", 1, "$10.00"))
        self.calc.tree.selection_set("item_del")
        
        # Simulate Delete key logic (calling the lambda target directly or simulating event)
        # Since we bound lambda e: self.delete_entry(), we can just call delete_entry
        # Or better, trigger the event if possible. But delete_entry is the target.
        self.calc.delete_entry()
        
        # Verify empty
        self.assertEqual(len(self.calc.tree.get_children()), 0)

if __name__ == '__main__':
    unittest.main()
