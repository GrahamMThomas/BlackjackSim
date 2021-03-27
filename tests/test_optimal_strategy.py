import pytest
from lib.cards.blackjack_hand import BlackjackHand
from lib.cards.card import Card
from lib.cards.card_suit import CardSuit
from lib.cards.card_value import CardValue
from lib.cards.shoe import Shoe
from lib.game.blackjack_action import BlackjackAction
from lib.game.driver import GameDriver
from lib.game.player import Player
from lib.strategies.optimal_strategy import OptimalStrategy
from lib.strategies.i_strategy import IStrategy


@pytest.fixture()
def game():
    shoe = Shoe()
    game = GameDriver(shoe, Player("Test", OptimalStrategy()))
    game.dealer_card = Card(CardValue.King, CardSuit.Spades)
    return game


@pytest.fixture()
def strat():
    return OptimalStrategy()


class TestOptimalStrategy:
    def test_surrender_hand(self, game: GameDriver, strat: IStrategy):
        hand = BlackjackHand.from_string("J♣,6♥")
        action = strat.get_action(game, hand)
        assert action == BlackjackAction.Surrender