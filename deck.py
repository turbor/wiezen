from random import randint

class NotCardError(Exception):
    def __init__(self,message):
        self.message = message

class Deck():
    def __init__(self):
        self.cards=[]
        self.newdeck()


    def newdeck(self):
        # In magic, and some card games, you’ll often hear people refer to something called new deck order.
        # New deck order simply refers to the order a deck of cards comes in straight out of the box before
        # its been handled, cut, or shuffled.
        # From the face of the deck, meaning you’re looking at the faces of the cards, you’ll find the:
        #
        #     Joker 1
        #     Joker 2
        #     Ace of Spades
        #     2 of Spades
        #     3 of Spades
        #     4 of Spades
        #     5 of Spades
        #     6 of Spades
        #     7 of Spades
        #     8 of Spades
        #     9 of Spades
        #     10 of Spades
        #     Jack of Spades
        #     Queen of Spades
        #     King of Spades
        #     Ace of Diamonds
        #     2 of Diamonds
        #     3 of Diamonds
        #     4 of Diamonds
        #     5 of Diamonds
        #     6 of Diamonds
        #     7 of Diamonds
        #     8 of Diamonds
        #     9 of Diamonds
        #     10 of Diamonds
        #     Jack of Diamonds
        #     Queen of Diamonds
        #     King of Diamonds
        #     King of Clubs
        #     Queen of Clubs
        #     Jack of Clubs
        #     10 of Clubs
        #     9 of Clubs
        #     8 of Clubs
        #     7 of Clubs
        #     6 of Clubs
        #     5 of Clubs
        #     4 of Clubs
        #     3 of Clubs
        #     2 of Clubs
        #     Ace of Clubs
        #     King of Hearts
        #     Queen of Hearts
        #     Jack of Hearts
        #     10 of Hearts
        #     9 of Hearts
        #     8 of Hearts
        #     7 of Hearts
        #     6 of Hearts
        #     5 of Hearts
        #     4 of Hearts
        #     3 of Hearts
        #     2 of Hearts
        #     Ace of Hearts
        #     Ad card 1
        #     Ad card 2
        #
        # Here we ignore jokers and ad cards
        self.cards.clear()
        for cardpip in ['S','D']: # spades,hearts,clubs,diamonds
            for cardval in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']:
                self.cards.append(cardpip+cardval)
        for cardpip in ['C','H']: # spades,hearts,clubs,diamonds
            for cardval in ['A','2','3','4','5','6','7','8','9','10','J','Q','K'].__reversed__() :
                self.cards.append(cardpip+cardval)

    def shufle(self):
        for i in range(len(self.cards)):
            j = randint(0,len(self.cards)-2)
            if j >= i:
                j = j + 1
            self.cards[i] , self.cards[j] = self.cards[j] , self.cards[i]

    def takeUppercard(self):
        val=''
        try:
            val=self.cards.pop()
        except:
            pass
        return val

    def clear(self):
        self.cards = []

    def addCard(self,card):
        if len(card)<2 or len(card)>3:
            raise NotCardError("{} is not a valid card".format(card))
        if not card[0] in ['C','S','H','D']:
            raise NotCardError("{} is not a valid card".format(card))
        self.cards.append(card)

    def removeCard(self,card):
        if len(card)<2 or len(card)>3:
            raise NotCardError("{} is not a valid card".format(card))
        if not card[0] in ['C','S','H','D']:
            raise NotCardError("{} is not a valid card".format(card))
        self.cards.remove(card)


if __name__ == "__main__":
    a = Deck()
    a.shufle()
    print(a)