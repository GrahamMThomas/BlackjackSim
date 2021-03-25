from enum import Enum


class CardSuit(Enum):
    Spades = 1
    Hearts = 2
    Clubs = 3
    Diamonds = 4

    def _get_symbol_map(self):
        symbols = {
            self.Hearts: "♥",
            self.Diamonds: "♦",
            self.Spades: "♠",
            self.Clubs: "♣",
        }
        return symbols

    @classmethod
    def from_string(cls, symbol: str):
        if symbol == "♥":
            return cls.Hearts
        elif symbol == "♦":
            return cls.Diamonds
        elif symbol == "♠":
            return cls.Spades
        elif symbol == "♣":
            return cls.Clubs

    def __repr__(self):
        symbols = self._get_symbol_map()

        return symbols[self]

    def __str__(self):
        symbols = self._get_symbol_map()

        return symbols[self]

    @staticmethod
    def list():
        return list(map(lambda c: c.value, CardSuit))