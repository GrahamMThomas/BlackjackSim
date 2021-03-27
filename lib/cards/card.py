from lib.cards.card_value import CardValue
from lib.cards.card_suit import CardSuit


class Card:
    def __init__(self, value: CardValue, suit: CardSuit):
        self.value = value
        self.suit = suit

    @classmethod
    def from_string(cls, card_string: str):
        symbol = card_string[-1]
        card_value = card_string[0:-1]
        return cls(CardValue.from_string(card_value), CardSuit.from_string(symbol))

    def __repr__(self):
        return f"Card<{CardValue(self.value)}{CardSuit(self.suit)}>"

    def __str__(self):
        return f"{str(CardValue(self.value))}{CardSuit(self.suit)}"

    def is_face_card(self):
        return self.value >= CardValue.Jack

    def blackjack_values(self):
        if self.value <= CardValue.Ten:
            return [self.value]
        elif self.value <= CardValue.King:
            return [10]
        elif self.value == CardValue.Ace:
            return [1, 11]
        raise RuntimeError("Card Value could not be convert to integer")