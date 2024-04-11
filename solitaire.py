# Following https://bicyclecards.com/how-to-play/solitaire


SEP = 8 * " "
CARD_LEN = 5


class Random:
    def __init__(
        self, seed=0, cap=1, modulus=2**32, multiplier=1664525, increment=1013904223
    ):
        """Taking default values from 'Numerical Recipes'"""
        self.cap = cap
        self.seed = seed
        self.modulus = modulus
        self.multiplier = multiplier
        self.increment = increment

    def randrange(self, cap):
        """Linear congruential generator for Pseudo-Random Number generation
        returns Z in [0, cap-1]"""
        self.cap = cap
        self.seed = (self.multiplier * self.seed + self.increment) % self.modulus
        return int(self.cap * self.seed / self.modulus)


class Card:
    def __init__(self, rank, suit, visible=False):
        self.rank = rank
        self.suit = suit
        self.visible = visible

    def set_visibility(self, visibility):
        self.visible = visibility

    def __str__(self):
        return (
            f"{self.rank}_{self.suit}".center(CARD_LEN)
            if self.visible
            else "x".center(CARD_LEN)
        )


class Deck:
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["♥", "♠", "♣", "♦"]

    def __init__(self, random_seed):
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
        self.shuffle(random_seed)

    def deal(self):
        return self.cards.pop()

    def is_available(self):
        return len(self.cards) != 0

    def shuffle(self, s=2130):
        """Fischer-Yates Shuffle"""
        r = Random(s)
        i = 52
        while i > 1:
            i -= 1
            j = r.randrange(i)
            self.cards[j], self.cards[i] = self.cards[i], self.cards[j]


class Tableau:
    def __init__(self, deck):
        self.piles = [[deck.deal() for _ in range(i)] for i in range(1, 8)]
        for i, pile in enumerate(self.piles):
            pile[i].set_visibility(True)

    def get_cards(self, pile_ind, start_card_ind):
        return self.piles[pile_ind][start_card_ind:]

    def add_card(self, pile_ind, card):
        self.piles[pile_ind].append(card)

    def remove_cards(self, pile_ind, start_card_ind):
        self.piles[pile_ind] = self.piles[pile_ind][:start_card_ind]
        try:
            self.piles[pile_ind][start_card_ind - 1].set_visibility(True)
        except IndexError:
            pass

    def move_cards(self, dest_pile_ind, source_pile_ind, source_start_card_ind):
        cards = self.piles[source_pile_ind][source_start_card_ind:]
        self.piles[source_pile_ind] = self.piles[source_pile_ind][
            :source_start_card_ind
        ]
        self.piles[dest_pile_ind].extend(cards)
        try:
            self.piles[source_pile_ind][source_start_card_ind - 1].set_visibility(True)
        except IndexError:
            pass

    def __str__(self):
        header = (
            SEP.join(
                [" ".center(CARD_LEN)] + [str(i).center(CARD_LEN) for i in range(1, 8)]
            )
            + "\n"
        )

        lines = []
        for i in range(max([len(p) for p in self.piles])):
            line = [str(i + 1).center(CARD_LEN)]
            for j in range(7):
                if len(self.piles[j]) > i:
                    line.append(str(self.piles[j][i]))
                else:
                    if i == 0:
                        line.append("-".center(CARD_LEN))
                    else:
                        line.append(" ".center(CARD_LEN))
            lines.append(SEP.join(line))

        return "Tableau:\n" + header + "\n".join(lines)


class Foundations:
    def __init__(self):
        self.piles = {suit: -1 for suit in Deck.suits}
        self.completed = False

    def add_to_pile(self, suit, n):
        assert n + self.piles[suit] <= 12
        self.piles[suit] += n

        for _, rank_n in self.piles.items():
            if rank_n != 12:
                break
        else:
            self.completed = True

    def get_filled(self, suit):
        return self.piles[suit]

    def __str__(self):
        pile_tops = []
        for suit, rank_n in self.piles.items():
            if rank_n == 12:
                pile_tops.append("+".center(CARD_LEN))
            elif rank_n >= 0:
                rank = Deck.ranks[rank_n]
                pile_tops.append(str(Card(rank, suit, True)))
            else:
                pile_tops.append("x".center(CARD_LEN))

        return "Foundations:\n" + SEP.join(pile_tops)


class Reserve:
    def __init__(self, deck):
        self.waste = []
        self.stock = []
        while deck.is_available():
            self.stock.append(deck.deal())

    def get(self):
        return self.stock[-1]

    def pop(self):
        return self.stock.pop()

    def reveal(self):
        self.stock[-1].set_visibility(True)

    def discard(self):
        if self.waste:
            self.waste[-1].set_visibility(False)

        self.waste.append(self.pop())
        if not self.stock:
            self.waste[-1].set_visibility(False)
            self.stock = self.waste[::-1].copy()
            self.waste = []

    def is_revealed(self):
        return self.stock[-1].visible

    def __str__(self):
        return (
            "Stock:\n"
            + str(self.stock[-1])
            + SEP
            + "\nWaste:\n"
            + (str(self.waste[-1]) if self.waste else "-".center(CARD_LEN))
        )


class Table:
    def __init__(self, seed):
        deck = Deck(seed)
        self.tableau = Tableau(deck)
        self.reserve = Reserve(deck)
        self.foundations = Foundations()
        self.n_moves = 0

    def play(self):
        print("Welcome to Solitaire in the Terminal!!")
        while True:
            print(self)
            choice = self.get_user_move()
            if choice == "0":
                print("Thank you for playing!")
                break
            elif choice == "4":
                self.reserve.discard()
            elif choice == "3":
                self.reserve.reveal()
            elif choice == "2":
                self.move_to_foundation()
            elif choice == "1":
                self.move_to_tableau()

            if self.foundations.completed:
                print(f"Congratulations, you have won the game in {self.n_moves}!!")
                break

            self.n_moves += 1  # handle reveal separately?

    def get_user_move(self):
        revealed = self.reserve.is_revealed()
        print(
            "1. move to tableau",
            "2. move to foundation",
            sep="\n",
        )
        if not revealed:
            print("3. reveal from stock pile")
        else:
            print("4. discard from stock pile")
        while True:
            choice = input("Select your option number or type 'quit': ")
            if choice == "quit":
                return "0"
            elif "1" <= choice <= "2":
                return choice
            elif choice == "3" and not revealed:
                return choice
            elif choice == "4" and revealed:
                return choice
            else:
                print(
                    "Invalid choice - please enter a number corresponding to one of the given options"
                )

    def move_to_foundation(self):
        choice = self.get_user_choice_source()
        if choice == "1":
            while True:
                try:
                    source_pile_n, card_n = map(
                        int, input("Entering starting card<col row>: ").split()
                    )
                except ValueError:
                    print("Invalid format. Enter as <col_number row_number>")
                    continue

                cards = table.tableau.get_cards(source_pile_n - 1, card_n - 1)
                if not cards[0].visible:
                    print("Invalid start card")
                else:
                    for card in cards:
                        if card.suit != cards[0].suit:
                            print("Cards not same suit")
                    else:
                        break
            if (
                Deck.ranks.index(cards[-1].rank)
                != self.foundations.get_filled(cards[0].suit) + 1
            ):
                print("Foundation missing prior cards")
                return

            self.tableau.remove_cards(source_pile_n - 1, card_n - 1)
            self.foundations.add_to_pile(cards[0].suit, len(cards))
        else:
            card = self.reserve.get()
            if (
                Deck.ranks.index(card.rank)
                != self.foundations.get_filled(card.suit) + 1
            ):
                print("Foundation missing prior cards")
                return

            self.reserve.pop()
            self.foundations.add_to_pile(card.suit, 1)

    def get_user_choice_source(self):
        revealed = self.reserve.is_revealed()
        if not revealed:
            return "1"

        print("1. move from tableau", "2. move from stock pile", sep="\n")
        while True:
            choice = input("Select your option number: ")
            if choice == "1":
                return choice
            elif choice == "2" and revealed:
                return choice
            else:
                print(
                    "Invalid choice - please enter a number corresponding to one of the given options"
                )

    def move_to_tableau(self):
        choice = self.get_user_choice_source()
        if choice == "1":
            while True:
                try:
                    source_pile_n, source_card_n = map(
                        int, input("Enter starting card<col row>: ").split()
                    )
                except ValueError:
                    print("Invalid format. Enter as <col_number row_number>")
                    continue

                cards = table.tableau.get_cards(source_pile_n - 1, source_card_n - 1)
                if not cards[0].visible:
                    print("Invalid start card")
                else:
                    dest_pile_n = int(input("Enter destination pile: "))
                    try:
                        card = self.tableau.get_cards(dest_pile_n - 1, -1)[0]

                        if (
                            Deck.ranks.index(cards[0].rank)
                            != Deck.ranks.index(card.rank) - 1
                        ):
                            print("Prior card not available in destination pile")
                        else:
                            break
                    except IndexError:
                        if Deck.ranks.index(cards[0].rank) != 12:
                            print("Only K can be moved to empty pile")
                        else:
                            break

            self.tableau.move_cards(
                dest_pile_n - 1, source_pile_n - 1, source_card_n - 1
            )
        else:
            card = self.reserve.get()

            while True:
                dest_pile_n = int(input("Enter destination pile: "))
                try:
                    dest_pile_card = self.tableau.get_cards(dest_pile_n - 1, -1)[0]
                    if (
                        Deck.ranks.index(card.rank)
                        != Deck.ranks.index(dest_pile_card.rank) - 1
                    ):
                        print("Prior card not available in destination pile")
                    else:
                        break
                except IndexError:
                    if Deck.ranks.index(card.rank) != 12:
                        print("Only K can be moved to empty pile")
                    else:
                        break
            self.reserve.pop()
            self.tableau.add_card(dest_pile_n - 1, card)

    def __str__(self):
        return "\n".join(map(str, [self.foundations, self.tableau, self.reserve]))


if __name__ == "__main__":

    seed = int(input("Enter an integer that will determine the order of your deck: "))
    table = Table(seed)
    table.play()
