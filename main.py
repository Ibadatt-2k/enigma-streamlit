from enigma.rotor import Rotor
from enigma.plugboard import Plugboard
from enigma.reflector import Reflector
from enigma.machine import EnigmaMachine

def test_enigma():
    # Define 3 rotors (right to left) with initial position 'A'
    rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch='Q', position='A')
    rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", notch='E', position='A')
    rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", notch='V', position='A')

    # Reflector B wiring
    reflectorB = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

    # Plugboard connections
    plugboard = Plugboard([('A', 'G'), ('M', 'N'), ('T', 'Z')])

    # Create the Enigma machine with [right, middle, left] rotor order
    machine = EnigmaMachine([rotor3, rotor2, rotor1], reflectorB, plugboard)

    message = "HELLO WORLD"
    encrypted = machine.encrypt_message(message)
    print("Encrypted:", encrypted)

    # Reset machine to same initial state for decryption
    rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch='Q', position='A')
    rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", notch='E', position='A')
    rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", notch='V', position='A')
    machine2 = EnigmaMachine([rotor3, rotor2, rotor1], reflectorB, plugboard)

    decrypted = machine2.encrypt_message(encrypted)
    print("Decrypted:", decrypted)

if __name__ == "__main__":
    test_enigma()

from gui.gui import EnigmaGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = EnigmaGUI(root)
    root.mainloop()

