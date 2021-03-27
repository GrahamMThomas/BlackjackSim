from __future__ import annotations
from lib.strategies.i_strategy import IStrategy
from lib.cards.blackjack_hand import BlackjackHand
from lib.game.blackjack_action import BlackjackAction

from lib.cards.deck import Deck
from lib.cards.card_value import CardValue
import pandas

import typing

if typing.TYPE_CHECKING:
    from lib.game.driver import GameDriver


class BookStrategy(IStrategy):
    def __init__(self):
        self.hard_action_grid = self.get_hard_action_grid()
        self.soft_action_grid = self.get_soft_action_grid()

    def get_action(self, game: GameDriver, hand: BlackjackHand):
        if hand.is_splittable() and self.should_i_split(hand, game.dealer_card):
            return BlackjackAction.Split
        elif hand.is_soft():
            highest_value = hand.get_hand_total()
            return self.soft_action_grid.loc[highest_value][game.dealer_card.value]
        else:  # Hard hand
            highest_value = hand.get_hand_total()
            return self.hard_action_grid.loc[highest_value][game.dealer_card.value]

    def get_bet(self, game: GameDriver):
        return game.minimum_bet

    def get_hard_action_grid(self):
        my_hands = range(4, 22)
        dealers_upcards = CardValue.list()
        grid = [[BlackjackAction.Stay for i in dealers_upcards] for j in my_hands]
        df = pandas.DataFrame(grid, index=my_hands, columns=dealers_upcards)
        df[df.index <= 8] = BlackjackAction.Hit
        df.loc[df.index == 9] = BlackjackAction.Hit
        df.loc[df.index == 9, list(range(2, 7))] = BlackjackAction.Double
        df.loc[df.index.isin([10, 11])] = BlackjackAction.Double
        df.loc[10, list(range(10, 15))] = BlackjackAction.Hit
        df.loc[11, CardValue.Ace] = BlackjackAction.Hit
        df.loc[(df.index >= 12) & (df.index <= 15), list(range(7, 15))] = BlackjackAction.Hit

        return df

    def should_i_split(self, hand, dealer_card):
        card = hand.cards[0]
        if card.value in [2, 3, 6, 7, 9] and dealer_card.value < 6:
            return True
        elif card.value in [8, CardValue.Ace]:
            return True
        return False

    def get_soft_action_grid(self):
        my_hands = range(13, 22)
        dealers_upcards = CardValue.list()
        grid = [[BlackjackAction.Stay for i in dealers_upcards] for j in my_hands]
        df = pandas.DataFrame(grid, index=my_hands, columns=dealers_upcards)
        df.loc[df.index <= 18] = BlackjackAction.Hit
        df.loc[df.index.isin(range(16, 19)), list(range(2, 7))] = BlackjackAction.Double
        return df