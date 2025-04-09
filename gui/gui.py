# NOTE: tkinter must be installed. If you're on Linux, you may need to install it via:
# sudo apt install python3-tk

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError as e:
    raise ImportError("The tkinter module is not installed. Please install it using your system's package manager (e.g., 'sudo apt install python3-tk' on Debian/Ubuntu).") from e

import threading
import math
import time
from enigma.rotor import Rotor
from enigma.reflector import Reflector
from enigma.plugboard import Plugboard
from enigma.machine import EnigmaMachine



class HoverButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["background"] = "#ff3eaa"

    def on_leave(self, e):
        self["background"] = self.defaultBackground

class EnigmaGUI:
    def __init__(self, root):
        self.root = root
        root.title("Enigma Machine Simulator")
        root.geometry("1024x768")
        root.minsize(800, 600)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        self.bg_canvas = tk.Canvas(root, bg="#1b1039", highlightthickness=0)
        self.bg_canvas.grid(row=0, column=0, sticky="nsew")

        self.frame = tk.Frame(self.bg_canvas, bg="#2e2547", bd=0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = tk.Label(self.frame, text="Enigma Machine Simulator", fg="white", bg="#2e2547",
                                     font=("Segoe UI", 20, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))

        tk.Label(self.frame, text="Input Message:", fg="white", bg="#2e2547",
                 font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=20)
        self.input_text = tk.Text(self.frame, height=2, width=45, bg="#18122B", fg="white",
                                  font=("Segoe UI", 10), insertbackground="white", relief="flat")
        self.input_text.grid(row=2, column=0, columnspan=3, padx=20, pady=5)

        tk.Label(self.frame, text="Plugboard Pairs (e.g. A-G,M-N):", fg="white", bg="#2e2547",
                 font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky="w", padx=20)
        self.plugboard_entry = tk.Entry(self.frame, width=47, bg="#18122B", fg="white",
                                        font=("Segoe UI", 10), insertbackground="white", relief="flat")
        self.plugboard_entry.grid(row=4, column=0, columnspan=3, padx=20, pady=5)

        tk.Label(self.frame, text="Rotor Positions (e.g. A A A):", fg="white", bg="#2e2547",
                 font=("Segoe UI", 10, "bold")).grid(row=5, column=0, sticky="w", padx=20)
        self.rotor_pos_entry = tk.Entry(self.frame, width=20, bg="#18122B", fg="white",
                                        font=("Segoe UI", 10), insertbackground="white", relief="flat")
        self.rotor_pos_entry.grid(row=6, column=0, columnspan=3, padx=20, pady=5)

        self.available_rotors = {
            "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q'),
            "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E'),
            "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V'),
            "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J'),
            "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", 'Z')
        }

        tk.Label(self.frame, text="Rotor Selection (Right → Left):", fg="white", bg="#2e2547",
                 font=("Segoe UI", 10, "bold")).grid(row=7, column=0, sticky="w", padx=20)
        self.rotor_right = ttk.Combobox(self.frame, values=list(self.available_rotors.keys()), state='readonly', width=10)
        self.rotor_middle = ttk.Combobox(self.frame, values=list(self.available_rotors.keys()), state='readonly', width=10)
        self.rotor_left = ttk.Combobox(self.frame, values=list(self.available_rotors.keys()), state='readonly', width=10)
        self.rotor_right.grid(row=8, column=0, padx=(20, 5), pady=5)
        self.rotor_middle.grid(row=8, column=1, padx=5, pady=5)
        self.rotor_left.grid(row=8, column=2, padx=(5, 20), pady=5)
        self.rotor_right.set("I")
        self.rotor_middle.set("II")
        self.rotor_left.set("III")

        self.encrypt_btn = HoverButton(self.frame, text="Encrypt", command=self.encrypt,
                                     font=("Segoe UI", 12, "bold"), bg="#ff6ec7", fg="white",
                                     relief="flat", padx=10, pady=5)
        self.encrypt_btn.grid(row=9, column=0, columnspan=1, pady=(10, 5), padx=(20, 10))

        self.decrypt_btn = HoverButton(self.frame, text="Decrypt", command=self.decrypt,
                                     font=("Segoe UI", 12, "bold"), bg="#6eb9ff", fg="white",
                                     relief="flat", padx=10, pady=5)
        self.decrypt_btn.grid(row=9, column=1, columnspan=2, pady=(10, 5), padx=(10, 20))

        tk.Label(self.frame, text="Output Message:", fg="white", bg="#2e2547",
                 font=("Segoe UI", 10, "bold")).grid(row=10, column=0, sticky="w", padx=20)
        self.output_box = tk.Text(self.frame, height=2, width=45, bg="#18122B", fg="white",
                                  font=("Segoe UI", 10), insertbackground="white", relief="flat")
        self.output_box.grid(row=11, column=0, columnspan=3, padx=20, pady=(5, 20))

    def decrypt(self):
        # Same as encryption: user must input encrypted message + correct settings
        msg = self.input_text.get("1.0", tk.END).strip().upper()
        rotor_pos = self.rotor_pos_entry.get().split()
        plug_pairs = self.plugboard_entry.get().upper().split(',')

        if len(rotor_pos) != 3:
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, "Error: Enter 3 rotor positions (e.g., A A A)")
            return

        try:
            plugboard_pairs = [(p[0], p[2]) for p in plug_pairs if len(p) == 3 and p[1] == '-']
        except:
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, "Error: Invalid plugboard format")
            return

        r1_key = self.rotor_right.get()
        r2_key = self.rotor_middle.get()
        r3_key = self.rotor_left.get()

        rotor1 = Rotor(*self.available_rotors[r1_key], position=rotor_pos[2])
        rotor2 = Rotor(*self.available_rotors[r2_key], position=rotor_pos[1])
        rotor3 = Rotor(*self.available_rotors[r3_key], position=rotor_pos[0])
        reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        plugboard = Plugboard(plugboard_pairs)

        machine = EnigmaMachine([rotor3, rotor2, rotor1], reflector, plugboard)
        decrypted = machine.encrypt_message(msg)

        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, decrypted)

    def encrypt(self):
        msg = self.input_text.get("1.0", tk.END).strip().upper()
        rotor_pos = self.rotor_pos_entry.get().split()
        plug_pairs = self.plugboard_entry.get().upper().split(',')

        if len(rotor_pos) != 3:
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, "Error: Enter 3 rotor positions (e.g., A A A)")
            return

        try:
            plugboard_pairs = [(p[0], p[2]) for p in plug_pairs if len(p) == 3 and p[1] == '-']
        except:
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, "Error: Invalid plugboard format")
            return

        r1_key = self.rotor_right.get()
        r2_key = self.rotor_middle.get()
        r3_key = self.rotor_left.get()

        rotor1 = Rotor(*self.available_rotors[r1_key], position=rotor_pos[2])
        rotor2 = Rotor(*self.available_rotors[r2_key], position=rotor_pos[1])
        rotor3 = Rotor(*self.available_rotors[r3_key], position=rotor_pos[0])
        reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        plugboard = Plugboard(plugboard_pairs)

        machine = EnigmaMachine([rotor3, rotor2, rotor1], reflector, plugboard)
        encrypted = machine.encrypt_message(msg)

        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, encrypted)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnigmaGUI(root)
    root.mainloop()
