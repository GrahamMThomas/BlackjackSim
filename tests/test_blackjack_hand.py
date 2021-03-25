from numpy import split
import pytest
from lib.cards.blackjack_hand import BlackjackHand
from lib.cards.card import Card
from lib.cards.card_value import CardValue
from lib.cards.card_suit import CardSuit


@pytest.fixture()
def soft_hand():
    return BlackjackHand(
        [Card(CardValue.Ace, CardSuit.Spades), Card(CardValue.Six, CardSuit.Spades)], 27
    )


@pytest.fixture()
def hard_hand():
    return BlackjackHand(
        [Card(CardValue.King, CardSuit.Spades), Card(CardValue.Six, CardSuit.Spades)],
        13,
    )


@pytest.fixture()
def split_hand():
    return BlackjackHand(
        [Card(CardValue.Eight, CardSuit.Spades), Card(CardValue.Eight, CardSuit.Clubs)],
        7,
    )


@pytest.fixture()
def double_ace_hand():
    cards = []
    cards.append(Card(CardValue.Two, CardSuit.Spades))
    cards.append(Card(CardValue.Ace, CardSuit.Spades))
    cards.append(Card(CardValue.Four, CardSuit.Spades))
    cards.append(Card(CardValue.Ace, CardSuit.Clubs))
    hand = BlackjackHand(cards)

    return hand


@pytest.fixture()
def busted_hand():
    return BlackjackHand(
        [
            Card(CardValue.King, CardSuit.Spades),
            Card(CardValue.Eight, CardSuit.Clubs),
            Card(CardValue.Queen, CardSuit.Clubs),
        ],
        7,
    )


class TestBlackjackHand:
    def test_possible_values(cls, soft_hand: BlackjackHand):
        assert soft_hand.get_possible_values() == [7, 17]

    def test_possible_values_double_aces(cls, double_ace_hand: BlackjackHand):
        assert double_ace_hand.get_possible_values() == [8, 18, 28]

    def test_valid_values_double_aces(cls, double_ace_hand: BlackjackHand):
        assert double_ace_hand.get_valid_values() == [8, 18]

    def test_is_soft(cls, soft_hand: BlackjackHand):
        assert soft_hand.is_soft()

    def test_is_splittable(cls, split_hand: BlackjackHand):
        assert split_hand.is_splittable()

    def test_is_busted(cls, busted_hand: BlackjackHand):
        assert busted_hand.is_busted()

    def test_split_hand(cls, split_hand: BlackjackHand):
        hand1, hand2 = BlackjackHand.split_hand(split_hand)
        assert len(hand1.cards) == 1
        assert hand1.cards[0] == split_hand.cards[0]