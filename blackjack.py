from lib.cards.shoe import Shoe
from lib.game.driver import GameDriver
from lib.game.player import Player
from lib.strategies.book_strategy import BookStrategy
from lib.strategies.optimal_strategy import OptimalStrategy
import matplotlib.pyplot as plt


def main():
    players = []
    hands = 100000
    initial_money = 100000
    table_minimum = 10

    for name in ["Caroline", "Tom"]:
        player = Player(name, BookStrategy(), money=initial_money)
        players.append(player)

    for name in ["Barbara", "Percy", "Daniel"]:
        player = Player(name, OptimalStrategy(), money=initial_money)
        players.append(player)

    shoe = Shoe(decks=8)
    driver = GameDriver(shoe, players, minimum_bet=table_minimum)
    for x in range(hands):
        if shoe.needs_shuffling():
            shoe.shuffle()
        driver.play_hand(x)
        print()

    for player in players:
        money_lost_per_hand_percentage = ((player.money - initial_money) / hands) / table_minimum
        odds = 0.50 + (money_lost_per_hand_percentage / 2)
        print(f"{player.name} Odds: {odds*100:.3f}%")
        plt.plot(range(0, hands + 1), player.money_history, label=player.name)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()