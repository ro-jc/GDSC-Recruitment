# Following https://bicyclecards.com/how-to-play/solitaire


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

    def __str__(self):
        return f"{self.rank}_{self.suit}" if self.visible else " x "


class Deck:
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["♥", "♠", "♣", "♦"]

    def __init__(self, random_seed):
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
        self.shuffle(random_seed)

    def deal(self):
        return self.cards.pop()

    def shuffle(self, s=2130):
        """Fischer-Yates Shuffle"""
        r = Random(s)
        i = 52
        while i > 1:
            i -= 1
            j = r.randrange(i)
            self.cards[j], self.cards[i] = self.cards[i], self.cards[j]


class Tableau:
    def __init__(self):
        self.piles = [[] for i in range(7)]

    def __str__(self):
        lines = []
        for i in range(max([len(p) for p in self.piles])):
            line = []
            for j in range(7):
                if len(self.piles[j]) > i:
                    line.append(str(self.piles[j][i]))
                else:
                    line.append("   ")
            lines.append("\t".join(line))

        return "\n".join(lines)


if __name__ == "__main__":
    pass
