from abc import ABC, abstractmethod
from lib.cards.blackjack_hand import BlackjackHand


class IStrategy(ABC):
    @abstractmethod
    def get_action(self, game: "GameDriver", hand: BlackjackHand):
        pass

    @abstractmethod
    def get_bet(self, game: "GameDriver"):
        pass
