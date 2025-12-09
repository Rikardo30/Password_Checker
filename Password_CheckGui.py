import tkinter as tk
from tkinter import ttk, messagebox

from Password_CheckLogic import (
    check_password_strength,
    strength_suggestions,
    randomize_improvement,
)

def main():
    # ---------------- Window setup ----------------
    root = tk.Tk()
    root.title("Password Void Checker")
    root.geometry("800x400")  # width x height (you can tweak this)
    # Tkinter variables to hold dynamic text
    

    # ---------------- Event handlers ----------------
    def on_check_password():

        # Use your logic functions
    
        # Clear any previous stronger password suggestion

    # ---------------- Layout (widgets) ----------------
    # Top frame for input
    
    # Strength display
    

    # Suggestions display
   
    # Stronger password section
   

    # ---------------- Run the app ----------------
        root.mainloop()


if __name__ == "__main__":
    main()