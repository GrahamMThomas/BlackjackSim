from lib.game.blackjack_action import BlackjackAction
from lib.game.player import Player
from lib.cards.shoe import Shoe
from lib.cards.card_suit import CardSuit
from lib.cards.card_value import CardValue
from lib.game.driver import GameDriver
import pytest
from lib.cards.blackjack_hand import BlackjackHand
from lib.strategies.book_strategy import BookStrategy
from lib.cards.card import Card


@pytest.fixture()
def game():
    shoe = Shoe()
    game = GameDriver(shoe, Player("Test", BookStrategy()))
    game.dealer_card = Card(CardValue.King, CardSuit.Spades)
    return game


@pytest.fixture()
def strat():
    return BookStrategy()


class TestBookStrategy:
    def test_under15_hard_hand(self, game: GameDriver, strat: BookStrategy):
        hand = BlackjackHand.from_string("4♣,7♥,4♥")
        action = strat.get_action(game, hand)
        assert action == BlackjackAction.Hit

    def test_under15_hard_hand2(self, game: GameDriver, strat: BookStrategy):
        hand = BlackjackHand.from_string("4♥,9♣")
        action = strat.get_action(game, hand)
        assert action == BlackjackAction.Hit

    def test_doubleaces(self, game: GameDriver, strat: BookStrategy):
        hand = BlackjackHand.from_string("A♠,A♦")
        action = strat.get_action(game, hand)
        assert action == BlackjackAction.Split