from lib.cards.card import Card
from lib.cards.card_value import CardValue
from lib.cards.card_suit import CardSuit


class Deck:
    def __init__(self):
        self.cards = []
        for val in CardValue.list():
            for suit in CardSuit.list():
                self.cards.append(Card(val, suit))
