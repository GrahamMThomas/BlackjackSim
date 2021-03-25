from enum import IntEnum


class CardValue(IntEnum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

    @classmethod
    def from_string(cls, card_value: str):
        if card_value == "J":
            return cls.Jack
        elif card_value == "Q":
            return cls.Queen
        elif card_value == "K":
            return cls.King
        elif card_value == "A":
            return cls.Ace
        else:
            return cls((int(card_value)))

    def __repr__(self):
        if self.value <= 10:
            return str(self.value)
        if self.value == 11:
            return "J"
        if self.value == 12:
            return "Q"
        if self.value == 13:
            return "K"
        if self.value == 14:
            return "A"

    def __str__(self):
        if self.value <= 10:
            return str(self.value)
        if self.value == 11:
            return "J"
        if self.value == 12:
            return "Q"
        if self.value == 13:
            return "K"
        if self.value == 14:
            return "A"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, CardValue))