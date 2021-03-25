from __future__ import annotations
import typing
from lib.cards.blackjack_hand import BlackjackHand
from lib.game.blackjack_action import BlackjackAction

if typing.TYPE_CHECKING:
    from lib.game.driver import GameDriver


class HouseStrategy:
    def __init__(self, dealer_hits_soft_17=True):
        self.dealer_hits_soft_17 = dealer_hits_soft_17

    def get_action(self, game: GameDriver, hand: BlackjackHand):
        if hand.is_soft():
            if hand.get_hand_total() >= 17 + (1 if self.dealer_hits_soft_17 else 0):
                return BlackjackAction.Stay
            else:
                return BlackjackAction.Hit
        else:
            if hand.get_hand_total() >= 17:
                return BlackjackAction.Stay
            else:
                return BlackjackAction.Hit

    def get_bet(self, game: GameDriver):
        raise NotImplementedError()