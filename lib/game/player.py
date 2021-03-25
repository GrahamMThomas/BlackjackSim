from __future__ import annotations
from lib.strategies.i_strategy import IStrategy
from lib.cards.blackjack_hand import BlackjackHand
from lib.game.blackjack_action import BlackjackAction
from lib.cards.card import Card

import typing

if typing.TYPE_CHECKING:
    from lib.game.driver import GameDriver


class NoMoneyBucko(RuntimeError):
    pass


class Player:
    def __init__(self, name: str, strategy: IStrategy, money=100):
        self.name = name
        self.strategy = strategy
        self.money = money
        self.hands = []
        self.money_history = [self.money]

    def get_house_hand(self):
        return self.hands[0]

    def get_dealt(self, hand: BlackjackHand):
        self.hands = [hand]

    def add_money(self, value):
        self.money += value

    def remove_money(self, value):
        if self.money < value:
            raise NoMoneyBucko()

        self.money -= value

    def get_action(self, game: GameDriver, hand: BlackjackHand):
        if hand.is_busted():
            return BlackjackAction.Bust
        return self.strategy.get_action(game, hand)

    def get_initial_bet(self, game):
        bet = self.strategy.get_bet(game)
        self.remove_money(bet)
        return bet

    def get_showing_card(self):
        # Only ever called on dealer so hands[0] is only hand
        return self.hands[0].showing_card

    def record_money_value(self):
        self.money_history.append(self.money)

    def __repr__(self):
        return f"Player<name={self.name}, money={self.money}>"