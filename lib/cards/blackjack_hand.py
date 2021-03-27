from lib.cards.card import Card
import numpy as np
import itertools
from typing import List


class AddCardToLockedHand(RuntimeError):
    pass


class CantSplitAnythingBut2CardsBro(RuntimeError):
    pass


class InvalidCard(RuntimeError):
    pass


class BlackjackHand:
    def __init__(self, cards: List[Card], bet=10, locked=False, from_split=False):
        self.cards = cards
        self.showing_card = None
        if len(cards) == 2:
            self.showing_card = cards[1]
        self.locked = locked
        self.bet = bet
        self._from_split = from_split

    @classmethod
    def split_hand(cls, hand):
        if len(hand.cards) != 2:
            raise CantSplitAnythingBut2CardsBro()

        # Can't resplit Aces?
        return cls([hand.cards[0]], hand.bet, from_split=True), cls([hand.cards[1]], hand.bet, from_split=True)

    @classmethod
    def from_string(cls, comma_seperated_cards: str):
        card_strings = [x.strip() for x in comma_seperated_cards.split(",")]
        cards = []
        for card_str in card_strings:
            cards.append(Card.from_string(card_str))
        return cls(cards)

    def make_bet(self, value):
        self.bet = value
        return value

    def hit(self, card: Card):
        self._add_card(card)

    def double_up(self, card: Card):
        self.bet = self.bet * 2
        self._add_card(card)
        return self.bet

    def is_soft(self):
        return len(self.get_valid_values()) > 1

    def is_splittable(self):
        if len(self.cards) != 2:
            return False
        return self.cards[0].value == self.cards[1].value
    
    def is_surrenderable(self):
        if len(self.cards) == 2 and not self._from_split:
            return True
        return False

    def is_busted(self):
        return len(self.get_valid_values()) == 0

    def is_blackjack(self):
        return len(self.cards) == 2 and self.get_hand_total() == 21

    def lock_cards(self):
        self.locked = True

    def get_hand_total(self):
        valid_values = self.get_valid_values()
        if len(valid_values) == 0:
            return min(self.get_possible_values())
        return valid_values[-1]

    def get_valid_values(self):
        return [x for x in self.get_possible_values() if x <= 21]

    def get_possible_values(self):
        card_values = [x.blackjack_values() for x in self.cards]
        possible = [sum(x) for x in itertools.product(*card_values)]
        possible = list(set(possible))
        possible.sort()
        return possible

    def _add_card(self, card: Card):
        if self.locked:
            raise AddCardToLockedHand()
        if card is None:
            raise InvalidCard()

        self.cards.append(card)

    def __repr__(self):
        return f"BlackjackHand<cards={','.join([str(x) for x in self.cards])}>"
