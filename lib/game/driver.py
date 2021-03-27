from lib.cards.blackjack_hand import BlackjackHand
from lib.game.player import NoMoneyBucko, Player
from lib.cards.shoe import Shoe
from lib.strategies.house_strategy import HouseStrategy
from lib.game.blackjack_action import BlackjackAction
from lib.config.ruleset import Ruleset
from typing import List, Tuple
from tabulate import tabulate


class GameDriver:
    def __init__(self, shoe: Shoe, players: List[Player], minimum_bet=10):
        self.shoe = shoe
        self.players = players
        self.house = Player("House", HouseStrategy(), 10000000)
        self.dealer_card = None
        self.hand_stack = []
        self.minimum_bet = minimum_bet

    def play_hand(self, id=0):
        print(f"####### Playing Hand #{id} ######################")
        finished_hands = []

        # Check shoe to make sure it has enough cards
        for player in self.players:
            try:
                bet = player.get_initial_bet(self)
            except NoMoneyBucko as ex:
                continue

            # I don't think dealing two cards in this order will change any odds
            hand = BlackjackHand([self.shoe.deal_card(), self.shoe.deal_card()], bet)
            player.get_dealt(hand)
            self.hand_stack.append((player, hand))

        dealer_hand = BlackjackHand([self.shoe.deal_card(), self.shoe.deal_card()], 0)
        self.house.get_dealt(dealer_hand)
        self.dealer_card = self.house.get_showing_card()

        self.hand_stack.insert(0, (self.house, dealer_hand))

        last_hand = None
        # While not everyone has stayed/busted
        while self.hand_stack and not dealer_hand.is_blackjack():
            player, hand = self.hand_stack.pop()
            if last_hand != hand:
                print(f"{hand}:")
                last_hand = hand
            action = player.get_action(self, hand)
            self.render_action(player, hand, action)
            if action in [
                BlackjackAction.Double,
                BlackjackAction.Stay,
                BlackjackAction.Bust,
                BlackjackAction.Surrender,
            ]:
                finished_hands.append((player, hand))

        if dealer_hand.is_blackjack():
            finished_hands = self.hand_stack
            self.hand_stack = []

        # Calculate
        self.payout(finished_hands, dealer_hand)
        for player in self.players:
            player.record_money_value()

    def render_action(self, player: Player, hand: BlackjackHand, action: BlackjackAction):
        if action == BlackjackAction.Hit:
            card = self.shoe.deal_card()
            hand.hit(card)
            print(f"\tHits {card}")
            self.hand_stack.append((player, hand))
        elif action == BlackjackAction.Double:
            player.remove_money(hand.bet)
            card = self.shoe.deal_card()
            hand.double_up(card)
            print(f"\tDoubles {card}")
        elif action == BlackjackAction.Split:
            player.remove_money(hand.bet)
            hand1, hand2 = BlackjackHand.split_hand(hand)
            hand1.hit(self.shoe.deal_card())
            hand2.hit(self.shoe.deal_card())
            print(f"Split {hand1} {hand2}")
            self.hand_stack.append((player, hand1))
            self.hand_stack.append((player, hand2))
        elif action == BlackjackAction.Stay:
            pass
        elif action == BlackjackAction.Bust:
            pass
        elif action == BlackjackAction.Surrender:
            if not Ruleset.rules().get("late_surrender"):
                raise RuntimeError("Late Surrender is not Allowed!")
            player.add_money(hand.bet / 2)
            print(f"Surrendered! +{hand.bet / 2}")
        else:
            raise RuntimeError("Dunno how to handle this Action")

    def payout(self, hands: List[Tuple[Player, BlackjackHand]], dealer_hand: BlackjackHand):
        dealer_total = dealer_hand.get_hand_total()

        print("\nResults:")
        print(f"Hand - {dealer_hand} - {dealer_total}")
        summary_table = []
        for player, hand in hands:
            hand_summary = []
            player_total = hand.get_hand_total()
            if player == self.house:
                continue

            hand_summary += [
                player.name,
                ",".join([str(x) for x in hand.cards]),
                hand.get_hand_total(),
            ]
            if dealer_hand.is_blackjack():
                if hand.is_blackjack():
                    player.add_money(hand.bet)
                    hand_summary.append("Bump")
                    hand_summary.append(0)
                else:
                    hand_summary.append("Got jacked!")
                    hand_summary.append(-1 * hand.bet)
            else:
                if hand.is_busted():
                    hand_summary.append("Busted")
                    hand_summary.append(-1 * hand.bet)
                elif hand.is_blackjack():
                    hand_summary.append("Blackjack")
                    blackjack_win = (
                        1.5 if Ruleset.rules().get("blackjack_pays_3_to_2", False) else 1.2
                    ) * hand.bet
                    hand_summary.append(blackjack_win)
                    player.add_money(blackjack_win + hand.bet)

                elif dealer_total > 21:
                    player.add_money(hand.bet * 2)  # original and winnings
                    hand_summary.append("Dealer Busted!")
                    hand_summary.append(hand.bet)

                elif dealer_total > player_total:
                    hand_summary.append("Dealer wins")
                    hand_summary.append(-1 * hand.bet)
                elif player_total > dealer_total:
                    player.add_money(hand.bet * 2)
                    hand_summary.append("In the money")
                    hand_summary.append(hand.bet)
                elif player_total == dealer_total:
                    player.add_money(hand.bet)
                    hand_summary.append("Bump")
                    hand_summary.append(0)
            summary_table.append(hand_summary)
        print(tabulate(summary_table))