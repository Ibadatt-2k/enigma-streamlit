# reflector.py
class Reflector:
    def __init__(self, wiring: str):
        self.wiring = wiring.upper()
        assert len(self.wiring) == 26, "Reflector wiring must be 26 characters"

    def reflect(self, c: str) -> str:
        index = ord(c.upper()) - ord('A')
        return self.wiring[index]
