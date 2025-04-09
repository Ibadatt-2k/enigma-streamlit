# plugboard.py
class Plugboard:
    def __init__(self, wiring_pairs=None):
        # Example: [('A', 'G'), ('M', 'N')]
        self.wiring = {}
        if wiring_pairs:
            for a, b in wiring_pairs:
                self.wiring[a.upper()] = b.upper()
                self.wiring[b.upper()] = a.upper()

    def swap(self, c: str) -> str:
        return self.wiring.get(c.upper(), c.upper())
