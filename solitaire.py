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

    def __str__(self):
        lines = []
        for i in range(max([len(p) for p in self.piles])):
            line = []
            for j in range(7):
                if len(self.piles[j]) > i:
                    line.append(str(self.piles[j][i]))
                else:
                    line.append(CARD_LEN * " ")
            lines.append(SEP.join(line))

        return "Tableau:\n" + "\n".join(lines)


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

    def reveal(self):
        self.stock[-1].set_visibility(True)

    def __str__(self):
        return (
            "Stock:\n"
            + str(self.stock[-1])
            + SEP
            + "\nWaste:\n"
            + (str(self.waste[0]) if self.waste else "-".center(CARD_LEN))
        )


class Table:
    def __init__(self, seed):
        deck = Deck(seed)
        self.tableau = Tableau(deck)
        self.reserve = Reserve(deck)
        self.foundations = Foundations()

    def __str__(self):
        return "\n".join(map(str, [self.foundations, self.tableau, self.reserve]))


if __name__ == "__main__":
    print("Welcome to Solitaire in the Terminal!!")
    seed = int(input("Enter an integer that will determine the order of your deck: "))
    table = Table(seed)

    print(table)
