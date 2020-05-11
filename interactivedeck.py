from deck import Deck

class InteractiveDeck(Deck):
    def __init__(self):
        super(InteractiveDeck, self).__init__()
        self.colored = True
        self.unicode = False

    def card2str(self,card):
        newcard = card[0]
        if self.unicode == True:
            # ["\u2663", "\u2660", "\u2666", "\u2665"]:  # Each suit: Clubs, Spades, Diamonds, Hearts
            newcard=("\u2660", "\u2665", "\u2663", "\u2666")[('S', 'H', 'C', 'D').index(card[0])]
        newcard = newcard + card[1:]
        if self.colored == True:
            if card[0]=='H' or card[0]=='D':
                newcard = "\033[1;31;48m{:>4s}\033[1;37;0m".format(newcard)
            else:
                newcard = "\033[1;30;48m{:>4s}\033[1;37;0m".format(newcard)
        else:
            newcard = "{:>4s}".format(newcard)
        return newcard

    def display(self):
        kaarten = list()
        for c in self.cards:
            kaarten.append("{}".format(self.card2str(c)))
        print("{} cards: {}".format(len(kaarten),''.join(kaarten)))

    def userPickCard(self):
        kaarten=list()
        nummers=list()
        for i,c in enumerate(self.cards):
            kaarten.append( "{}".format(self.card2str(c)) )
            nummers.append( "{:>4d}".format(i+1))
        while True:
            try:
                print(''.join(kaarten))
                print(''.join(nummers))
                userInput = int(input("Kaart nummer aub : "))
            except ValueError:
                print("Not an integer! Try again.")
                continue
            else:
                if userInput<1 or userInput>len(kaarten):
                    print("Geen geldig nummer")
                    continue
                return self.cards[userInput-1]


if __name__ == "__main__":
    d = InteractiveDeck()
    print(d.userPickCard())
    d.cards=['S3','S4','H5','HA','D10','S10','SJ']
    print(d.userPickCard())