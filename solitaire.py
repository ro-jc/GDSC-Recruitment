# Following https://bicyclecards.com/how-to-play/solitaire


class Card:
    def __init__(self, rank, suit, visible=False):
        self.rank = rank
        self.suit = suit
        self.visible = visible

    def __str__(self):
        return f"{self.rank}_{self.suit}" if self.visible else " x "


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
