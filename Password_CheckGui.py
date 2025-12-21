import tkinter as tk
from tkinter import *
from tkinter import messagebox
## Widgets = GUI elements like buttons, labels, text boxes, etc.
## Windows = The main container for the GUI application
from Password_CheckLogic import (
    check_password_strength,
    strength_suggestions,
    randomize_improvement,
)

def main():
    # ---------------- Window setup ----------------
    window = tk.Tk() #instance of window
    window.title("Void Password Manager")
    window.geometry("600x400")
    window.config(background= "Black")
    # Icon 
    void_icon = PhotoImage(file='void2.png')
    window.iconphoto(True, void_icon)
    # Tkinter variables to hold dynamic text
    

    # ---------------- Event handlers ----------------
    def on_test_strength():
        password = password_input.get()
        result = check_password_strength(password)
        strength_label.config(text=f'Strength: {result}')
        # suggestion logic
        suggestions = strength_suggestions(password)
        if suggestions:
            suggestions_label.config(text=f'Suggestions: {", ".join(suggestions)}')
    
        # Clear any previous stronger password suggestion

    # ---------------- Layout (widgets) ----------------
    #Label for title
    tittle_intro = Label(window,text="Password Void",
                         font=('Courier',17,'bold'),
                         fg='white',
                         bg='black')
    tittle_intro.pack(fill="x")
    # Input Label
    input_label = Label(window, text="[Enter Password]:",
                        fg="white",
                        bg="black")
    input_label.pack(anchor="w")
    # Top frame for input
    input_frame = Frame(window, bg='black', pady=20, padx=20)
    input_frame.pack()
    # Password input
    password_input = Entry(input_frame,
                           width= 40,
                        font=('Courier',12))
    password_input.pack(pady=(5, 10))
    # Strength display
    display_strength = Button(text= "Test Strength", command=on_test_strength)
    display_strength.pack()
    #Strength label
    strength_label = Label(window, text="", fg="white",bg="black")
    strength_label.pack(pady =(0, 10))
    
    # Suggestions display
    suggestions_label = Label(window, text="", fg="white", bg="black")
    suggestions_label.pack(pady=(0, 10))
    # Stronger password section
   

    # ---------------- Run the app ----------------
    window.mainloop() #place window on screen and listen for events


if __name__ == "__main__":
    main()