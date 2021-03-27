from __future__ import annotations
from lib.strategies.i_strategy import IStrategy
from lib.cards.blackjack_hand import BlackjackHand
from lib.game.blackjack_action import BlackjackAction

from lib.cards.deck import Deck
from lib.cards.card_value import CardValue
from lib.config.ruleset import Ruleset
import pandas

import typing

if typing.TYPE_CHECKING:
    from lib.game.driver import GameDriver


class OptimalStrategy(IStrategy):
    def __init__(self):
        self.df_hard = self.hard_totals_matrix()
        self.df_soft = self.soft_totals_matrix()
        self.df_split = self.splitting_matrix()
        self.df_surrender = self.surrender_matrix()

    def get_bet(self, game: GameDriver):
        return game.minimum_bet

    def get_action(self, game: GameDriver, hand: BlackjackHand):
        if (
            Ruleset.rules().get("late_surrender")
            and hand.is_surrenderable()
            and self.df_surrender.loc[hand.get_hand_total(), game.dealer_card.value]
        ):
            return BlackjackAction.Surrender
        elif hand.is_splittable() and self.df_split.loc[hand.cards[0].value, game.dealer_card.value]:
            return BlackjackAction.Split
        elif hand.is_soft():
            df = self.df_soft
            return df.loc[hand.get_hand_total(), game.dealer_card.value]
        else:
            df = self.df_hard
            return df.loc[hand.get_hand_total(), game.dealer_card.value]

    def hard_totals_matrix(self):
        my_hands = range(4, 22)
        dealers_upcards = CardValue.list()
        grid = [[BlackjackAction.Stay for i in dealers_upcards] for j in my_hands]
        df = pandas.DataFrame(grid, index=my_hands, columns=dealers_upcards)

        d = BlackjackAction.Double
        h = BlackjackAction.Hit
        s = BlackjackAction.Stay

        df.loc[df.index <= 9] = BlackjackAction.Hit
        df.loc[9] = [h, d, d, d, d, h, h, h, h, h, h, h, h]
        df.loc[10] = [d, d, d, d, d, d, d, h, h, h, h, h, h]
        df.loc[11] = BlackjackAction.Double
        df.loc[12] = [h, h, s, s, s, h, h, h, h, h, h, h, h]
        df.loc[(df.index >= 13) & (df.index <= 16), list(range(7, 15))] = BlackjackAction.Hit
        return df

    def soft_totals_matrix(self):
        my_hands = range(13, 22)
        dealers_upcards = CardValue.list()
        grid = [[BlackjackAction.Stay for i in dealers_upcards] for j in my_hands]
        df = pandas.DataFrame(grid, index=my_hands, columns=dealers_upcards)

        d = BlackjackAction.Double
        h = BlackjackAction.Hit
        s = BlackjackAction.Stay

        df.loc[19, 6] = d
        df.loc[18] = [d, d, d, d, d, s, s, h, h, h, h, h, h]
        df.loc[17] = [h, d, d, d, d, h, h, h, h, h, h, h, h]
        df.loc[16] = [h, h, d, d, d, h, h, h, h, h, h, h, h]
        df.loc[15] = [h, h, d, d, d, h, h, h, h, h, h, h, h]
        df.loc[14] = [h, h, h, d, d, h, h, h, h, h, h, h, h]
        df.loc[13] = [h, h, h, d, d, h, h, h, h, h, h, h, h]

        return df

    def splitting_matrix(self):
        my_hands = CardValue.list()
        dealers_upcards = CardValue.list()

        grid = [[False for i in dealers_upcards] for j in my_hands]
        df = pandas.DataFrame(grid, index=my_hands, columns=dealers_upcards)

        y = True
        n = False

        df.loc[CardValue.Ace] = True
        df.loc[CardValue.King] = False
        df.loc[CardValue.Queen] = False
        df.loc[CardValue.Jack] = False
        df.loc[CardValue.Ten] = False
        df.loc[CardValue.Nine] = [y, y, y, y, y, n, y, y, n, n, n, n, n]
        df.loc[CardValue.Eight] = True
        df.loc[CardValue.Seven, list(range(2, 8))] = True
        df.loc[CardValue.Six, list(range(2, 7))] = True
        df.loc[CardValue.Four, [5, 6]] = True
        df.loc[CardValue.Three, list(range(2, 8))] = True
        df.loc[CardValue.Two, list(range(2, 8))] = True

        return df

    def surrender_matrix(self):
        my_hands = range(4, 22)
        dealers_upcards = CardValue.list()
        grid = [[False for i in dealers_upcards] for j in my_hands]
        df = pandas.DataFrame(grid, index=my_hands, columns=dealers_upcards)

        df.loc[16, list(range(9, 15))] = True
        df.loc[15, list(range(10, 14))] = True
        return df