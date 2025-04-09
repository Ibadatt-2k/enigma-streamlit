# rotor.py
class Rotor:
    def __init__(self, wiring: str, notch: str, ring_setting: int = 0, position: str = 'A'):
        self.wiring = wiring
        self.notch = notch
        self.ring_setting = ring_setting % 26
        self.position = ord(position.upper()) - ord('A')

        self.reverse_wiring = [''] * 26
        for i, char in enumerate(wiring):
            self.reverse_wiring[ord(char) - ord('A')] = chr(i + ord('A'))

    def _shift(self, index):
        return (index + self.position - self.ring_setting) % 26

    def forward(self, c: str) -> str:
        index = self._shift(ord(c.upper()) - ord('A'))
        letter = self.wiring[index]
        out = (ord(letter) - ord('A') - self.position + self.ring_setting) % 26
        return chr((out + 26) % 26 + ord('A'))

    def backward(self, c: str) -> str:
        index = self._shift(ord(c.upper()) - ord('A'))
        letter = self.reverse_wiring[index]
        out = (ord(letter) - ord('A') - self.position + self.ring_setting) % 26
        return chr((out + 26) % 26 + ord('A'))

    def step(self):
        self.position = (self.position + 1) % 26

    def current_position(self) -> str:
        return chr(self.position + ord('A'))
