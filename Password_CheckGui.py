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
    window.geometry("850x550")
    window.config(background= "#333333")
    # Icon 
    void_icon = PhotoImage(file='void2.png')
    window.iconphoto(True, void_icon)
    # Tkinter variables to hold dynamic text
    # ---------------- Frames (Top + Bottom) ----------------
    top_frame = Frame(window, bg="#333333", height=260)
    top_frame.pack(fill="x")
    top_frame.pack_propagate(False)

    bottom_frame = Frame(window, bg="#2b2b2b", height=240)
    bottom_frame.pack(fill="both", expand=True)

    # --- Bottom split using GRID (perfect 50/50) ---
    bottom_frame.grid_propagate(False)

    bottom_frame.columnconfigure(0, weight=1, uniform="half")
    bottom_frame.columnconfigure(1, weight=0)              # divider
    bottom_frame.columnconfigure(2, weight=1, uniform="half")
    bottom_frame.rowconfigure(0, weight=1)

    left_bottom = Frame(bottom_frame, bg="#2b2b2b")
    left_bottom.grid(row=0, column=0, sticky="nsew")

    divider = Frame(bottom_frame, bg="white", width=2)
    divider.grid(row=0, column=1, sticky="nsew")           # IMPORTANT

    right_bottom = Frame(bottom_frame, bg="#2b2b2b")
    right_bottom.grid(row=0, column=2, sticky="nsew")
    # ---------------- Event handlers ----------------
    def on_test_strength():
        password = password_input.get()
        result = check_password_strength(password)
        strength_label.config(text=f'Strength: {result}')
        # suggestion logic
        suggestions = strength_suggestions(password)
        if suggestions:
            suggestions_label.config(text='Suggestions:\n' + "\n".join(suggestions))
    
        # Clear any previous stronger password suggestion

    # ---------------- Layout (widgets) ----------------
    #Label for title
    tittle_intro = Label(top_frame,text="Password Void",
                         font=('Courier',22,'bold'),
                         fg='#e102ef',
                         bg='#333333')
    tittle_intro.pack(fill="x")
    # Input Label
    input_label = Label(top_frame, text="[Enter Password]:",
                        fg="white",
                        bg="#333333")
    input_label.pack()
    # Top frame for input
    input_frame = Frame(top_frame, bg='#333333', pady=1, padx=7)
    input_frame.pack()
    # Password input
    password_input = Entry(input_frame,
                           show="*",
                           width= 40,
                        font=('Courier',12))
    password_input.pack(pady=(5, 10))
    # Strength display
    display_strength = Button(top_frame, text= "Test Strength", command=on_test_strength)
    display_strength.pack()
    #Strength label
    strength_label = Label(top_frame, text="", fg="#e102ef",bg="#333333")
    strength_label.pack(pady =(0, 10))
    
    # Suggestions display
    suggestions_label = Label(top_frame, text="", fg="white", bg="#333333", justify= "left")
    suggestions_label.pack(pady=(0, 10))
    # Stronger password section/left##########################
    ##########################################################
    stronger_passwordr = Label(left_bottom, 
                              text="Generate Stronger Password", 
                              fg="#e102ef",
                              bg="#2b2b2b",
                              font=('Courier',18,'bold'),
                              justify="center")
    stronger_passwordr.pack(padx=25, fill="x")
    # Stronger password section/right#########################
    ##########################################################
    stronger_passwordl = Label(right_bottom, 
                              text="Void Password Locker", 
                              fg="#e102ef",
                              bg="#2b2b2b",
                              font=('Courier',18,'bold'),
                              justify="center")
    stronger_passwordl.pack(padx=25, fill="x")
    # ---------------- Run the app ----------------
    window.mainloop() #place window on screen and listen for events


if __name__ == "__main__":
    main()