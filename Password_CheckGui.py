import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox

from Password_CheckLogic import (
    check_password_strength,
    strength_suggestions,
    randomize_improvement,
)

# vault backend functions
from Vault_Master import load_entries, add_entry, delete_entry, reset_vault


def main():
    # ---------------- Window setup ----------------
    window = tk.Tk()  # instance of window
    window.title("Void Password Manager")
    window.geometry("1150x700")
    window.config(background="#2b2b2b")
    # Icon
    void_icon = PhotoImage(file='void2.png')
    window.iconphoto(True, void_icon)

    # ---------------- Frames (Top + Bottom) ----------------
    top_frame = Frame(window, bg="#2b2b2b", height=260)
    top_frame.pack(fill="x")
    top_frame.pack_propagate(False)

    divider_h = Frame(window, bg="white", height=2)
    divider_h.pack(fill="x")

    bottom_frame = Frame(window, bg="#2b2b2b", height=240)
    bottom_frame.pack(fill="both", expand=True)

    # --- Bottom split using GRID ---
    bottom_frame.grid_propagate(False)

    bottom_frame.columnconfigure(0, weight=1, uniform="half")
    bottom_frame.columnconfigure(1, weight=0)              # divider
    bottom_frame.columnconfigure(2, weight=1, uniform="half")
    bottom_frame.rowconfigure(0, weight=1)

    left_bottom = Frame(bottom_frame, bg="#2b2b2b")
    left_bottom.grid(row=0, column=0, sticky="nsew")

    divider = Frame(bottom_frame, bg="white", width=2)
    divider.grid(row=0, column=1, sticky="nsew") # vertical divider

    right_bottom = Frame(bottom_frame, bg="#2b2b2b")
    right_bottom.grid(row=0, column=2, sticky="nsew")

    # ---------------- Vault state ----------------
    vault_unlocked = False
    vault_entries = []
    master_pw_cache = ""

    # ---------------- Event handlers ----------------
    def on_test_strength():
        password = password_input.get()
        result = check_password_strength(password)
        strength_label.config(text=f'Strength: {result}')
        # suggestion logic
        suggestions = strength_suggestions(password)
        if suggestions:
            suggestions_label.config(text='Suggestions:\n' + "\n".join(suggestions))

    def on_generate_stronger():
        password = password_input.get()
        stronger = randomize_improvement(password)
        Generated_PassResult.config(text=f"Stronger password:\n{stronger}")
        # Clear any previous stronger password suggestion

    # ---------------- Vault handlers ----------------
    def refresh_vault_list():
        vault_list.delete(0, END)
        for e in vault_entries:
            vault_list.insert(END, f"{e['site']} | {e['username']}")
## Unlocks Vault
    def on_unlock_vault():
        nonlocal vault_unlocked, vault_entries, master_pw_cache
        mp = master_password_input.get().strip()
        if not mp:
            messagebox.showwarning("Missing", "Enter your master password.")
            return
        vault_entries = load_entries(mp)
        if os.path.exists("vault_data.enc") and vault_entries == []:
            messagebox.showerror("Wrong Password", "That master password cannot unlock this vault.")
            return

        master_pw_cache = mp
        vault_unlocked = True
        vault_status.config(text="Unlocked", fg="lightgreen")
        refresh_vault_list()
## Locks Vault
    def on_lock_vault():
        nonlocal vault_unlocked, vault_entries, master_pw_cache
        vault_unlocked = False
        master_pw_cache = ""
        vault_entries = []
        vault_status.config(text="Locked", fg="orange")
        vault_list.delete(0, END)
## Add Entry to Vault
    def on_add_vault_entry():
        nonlocal vault_entries
        if not vault_unlocked:
            messagebox.showerror("Locked", "Unlock the vault first.")
            return

        site = site_input.get().strip()
        user = user_input.get().strip()
        pw = pass_input.get().strip()

        if not site or not user or not pw:
            messagebox.showwarning("Missing", "Fill in Site, Username, and Password.")
            return

        add_entry(master_pw_cache, site, user, pw)
        vault_entries = load_entries(master_pw_cache)
        refresh_vault_list()

        site_input.delete(0, END)
        user_input.delete(0, END)
        pass_input.delete(0, END)
## View selected entry's password
    def on_view_selected_password():
        if not vault_unlocked:
            messagebox.showerror("Locked", "Unlock the vault first.")
            return
        sel = vault_list.curselection()
        if not sel:
            messagebox.showwarning("Select", "Select an entry first.")
            return
        idx = sel[0]
        messagebox.showinfo("Saved Password", vault_entries[idx]["password"])
## Delete selected entry from vault
    def on_delete_selected_entry():
        nonlocal vault_entries
        if not vault_unlocked:
            messagebox.showerror("Locked", "Unlock the vault first.")
            return
        sel = vault_list.curselection()
        if not sel:
            messagebox.showwarning("Select", "Select an entry first.")
            return
        idx = sel[0]
        delete_entry(master_pw_cache, idx)
        vault_entries = load_entries(master_pw_cache) ##Need to adapt this to load entries alphabetically
        refresh_vault_list()
## Reset vault (deletes all entries)
    def on_reset_vault_gui():
        nonlocal vault_unlocked, vault_entries, master_pw_cache
        if not messagebox.askyesno(
            "Reset Vault",
            "This will permanently delete ALL saved passwords.\nThis cannot be undone.\n\nContinue?"
        ):
            return

        reset_vault()
        vault_unlocked = False
        master_pw_cache = ""
        vault_entries = []
        vault_status.config(text="Locked", fg="orange")
        vault_list.delete(0, END)
        messagebox.showinfo("Vault Reset", "Vault cleared. You can set a new master password now.")

    # ---------------- Layout (widgets) ----------------
    # Label for title
    tittle_intro = Label(top_frame, text="Password Void",
                         font=('Zen Dots', 24, 'bold'),
                         fg='#e102ef',
                         bg='#333333')
    tittle_intro.pack(fill="x")

    # Input Label
    input_label = Label(top_frame, text="[Enter Password]:",
                        fg="white",
                        bg="#2b2b2b")
    input_label.pack()

    # Top frame for input
    input_frame = Frame(top_frame, bg='#2b2b2b', pady=1, padx=7)
    input_frame.pack()

    # Password input
    password_input = Entry(input_frame,
                           bg="#333333",
                           fg="white",
                           show="*",
                           width=40,
                           font=('Courier', 12))
    password_input.pack(pady=(5, 10))

    # Strength display
    display_strength = Button(top_frame, text="Test Strength", command=on_test_strength)
    display_strength.pack()

    # Strength label
    strength_label = Label(top_frame, text="", fg="#e102ef", bg="#2b2b2b")
    strength_label.pack(pady=(0, 10))

    # Suggestions display
    suggestions_label = Label(top_frame, text="", fg="white", bg="#2b2b2b", justify="left")
    suggestions_label.pack(pady=(0, 10))

    # Stronger password section/left##########################
    ##########################################################
    stronger_passwordr = Label(left_bottom,
                              text="Password Enhancer",
                              fg="#e102ef",
                              bg="#2b2b2b",
                              font=('Zen Dots', 24, 'bold'),
                              justify="center")
    stronger_passwordr.pack(padx=25, fill="x")

    Generate_Password = Button(left_bottom, text="Generate", command=on_generate_stronger)
    Generate_Password.pack()

    Generated_PassResult = Label(left_bottom, text="", font=(16), fg="white", bg="#2b2b2b", justify="left")
    Generated_PassResult.pack(pady=(0, 10))

    # Stronger password section/right#########################
    ##########################################################
    stronger_passwordl = Label(right_bottom,
                              text="Password Locker",
                              fg="#e102ef",
                              bg="#2b2b2b",
                              font=('Zen Dots', 24, 'bold'),
                              justify="center")
    stronger_passwordl.pack(padx=25, fill="x")

    # ---------------- Vault widgets (ADDED) ----------------
    vault_status = Label(right_bottom, text="Locked", fg="orange", bg="#2b2b2b",
                         font=("Courier", 11, "bold"))
    vault_status.pack(pady=(5, 10))

    mp_frame = Frame(right_bottom, bg="#2b2b2b")
    mp_frame.pack(pady=(0, 10))

    Label(mp_frame, text="Master:", fg="white", bg="#2b2b2b", font=("Courier", 11)).pack(side="left")
    master_password_input = Entry(mp_frame, bg="#333333", fg="white", show="*", width=18, font=("Courier", 11))
    master_password_input.pack(side="left", padx=6)

    Button(mp_frame, text="Unlock", command=on_unlock_vault).pack(side="left", padx=4)
    Button(mp_frame, text="Lock", command=on_lock_vault).pack(side="left", padx=4)

    form_frame = Frame(right_bottom, bg="#2b2b2b")
    form_frame.pack(pady=(0, 10))

    Label(form_frame, text="Site:", fg="white", bg="#2b2b2b", font=("Courier", 11)).grid(row=0, column=0, sticky="w")
    site_input = Entry(form_frame, bg="#333333", fg="white", width=22, font=("Courier", 11))
    site_input.grid(row=0, column=1, padx=6, pady=2)

    Label(form_frame, text="User:", fg="white", bg="#2b2b2b", font=("Courier", 11)).grid(row=1, column=0, sticky="w")
    user_input = Entry(form_frame, bg="#333333", fg="white", width=22, font=("Courier", 11))
    user_input.grid(row=1, column=1, padx=6, pady=2)

    Label(form_frame, text="Pass:", fg="white", bg="#2b2b2b", font=("Courier", 11)).grid(row=2, column=0, sticky="w")
    pass_input = Entry(form_frame, show="*", bg="#333333", fg="white", width=22, font=("Courier", 11))
    pass_input.grid(row=2, column=1, padx=6, pady=2)

    Button(right_bottom, text="Add Entry", command=on_add_vault_entry).pack(pady=(0, 10))

    vault_list = Listbox(right_bottom, bg="#333333", fg="white", width=35, height=6, font=("Courier", 10))
    vault_list.pack(padx=10, pady=(0, 10), fill="both", expand=True)

    action_frame = Frame(right_bottom, bg="#2b2b2b")
    action_frame.pack(pady=(0, 10))

    Button(action_frame, text="View Password", command=on_view_selected_password).pack(side="left", padx=4)
    Button(action_frame, text="Delete Entry", command=on_delete_selected_entry).pack(side="left", padx=4)

    Button(right_bottom, text="Reset Vault", bg="#7a0000", fg="white", command=on_reset_vault_gui).pack(pady=(0, 10))

    # ---------------- Run the app ----------------
    window.mainloop()  # place window on screen and listen for events


if __name__ == "__main__":
    main()