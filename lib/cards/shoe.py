from lib.cards.deck import Deck
from lib.cards.card_value import CardValue
import random


class Shoe:
    def __init__(self, decks=1):
        decks = [Deck() for x in range(0, decks)]
        self.cards = []
        for deck in decks:
            self.cards += deck.cards
        self.discard = []
        self.adv_count = 0

        self.shuffle()

    def shuffle(self):
        self.cards += self.discard
        self.discard = []
        random.shuffle(self.cards)

    def deal_card(self):
        card = self.cards.pop()
        if card.value <= CardValue.Six:
            self.adv_count += 1
        elif card.value >= CardValue.Ten:
            self.adv_count -= 1
        self.discard.append(card)
        return card

    def needs_shuffling(self, shoe_shuffle_percent=0.30):
        return len(self.cards) / len(self.cards + self.discard) < shoe_shuffle_percent
