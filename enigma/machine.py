# machine.py
from enigma.plugboard import Plugboard
from enigma.rotor import Rotor
from enigma.reflector import Reflector

class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard=None):
        self.rotors = rotors  # List of rotors: [right, middle, left]
        self.reflector = reflector
        self.plugboard = plugboard if plugboard else Plugboard()

    def step_rotors(self):
        # Implements rotor stepping: right rotor steps every keypress
        rotate_next = True
        for i in range(len(self.rotors)):
            if rotate_next:
                self.rotors[i].step()
                rotate_next = self.rotors[i].notch == self.rotors[i].current_position()
            else:
                break

    def encrypt_letter(self, letter: str) -> str:
        if not letter.isalpha():
            return letter

        self.step_rotors()

        # Pass through plugboard
        letter = self.plugboard.swap(letter)

        # Forward pass through rotors (right → left)
        for rotor in self.rotors:
            letter = rotor.forward(letter)

        # Reflect
        letter = self.reflector.reflect(letter)

        # Backward pass through rotors (left → right)
        for rotor in reversed(self.rotors):
            letter = rotor.backward(letter)

        # Final plugboard swap
        return self.plugboard.swap(letter)

    def encrypt_message(self, message: str) -> str:
        result = ""
        for char in message:
            if char.isalpha():
                result += self.encrypt_letter(char.upper())
            else:
                result += char
        return result
