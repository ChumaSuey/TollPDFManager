import tkinter as tk
import sv_ttk
from gui.app import TollManagerApp

def main():
    root = tk.Tk()
    root.title("Toll PDF Manager")
    root.geometry("1400x800")

    # Fix for high DPI screens
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = TollManagerApp(root)
    app.pack(fill="both", expand=True)

    sv_ttk.set_theme("dark")

    root.mainloop()

if __name__ == "__main__":
    main()
