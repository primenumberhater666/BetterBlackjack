
import random
from random import randint 
from card import Card

class Sequence:
    def __init__(self, decks, cut):
        self.decks = decks # number of decks in play
        self.cut = cut     # number of cards to chop off (penetration)
        self.cards = []
        self.curr = 0      # index of current card at play   
        self.rc = 0

    # returns the total number of cards based on number of decks (trivial)
    def totalNumCards(self):
        return 52 * self.decks 

    # returns the number of cards left before shuffling (not including current)
    def cardsRemaining(self):
        return (self.totalNumCards() - self.cut) - self.curr
    
    # returns true count of current shoe
    def getTC(self):
        decks = self.cardsRemaining() / 52.0
        if decks == 0: return 0 
        return self.rc / decks

    # Increments the curr value to point to the next card in array. 
    def getNextCard(self):
        self.curr += 1 

    # Updates count
    def updateRC(self): 
        if self.cards[self.curr].value >= 2 and self.cards[self.curr].value <= 6:
            self.rc += 1
        elif self.cards[self.curr].value >= 10 or self.cards[self.curr].value == 1:
            self.rc -= 1 
    

    # generates new sequence of cards
    def shuffle(self):
        self.curr = 0 
        self.rc = 0 
        self.cards.clear()
        valueMap = {"2" : 2,
            "3" : 3,
            "4" : 4,
            "5" : 5, 
            "6" : 6,
            "7" : 7,
            "8" : 8,
            "9" : 9,
            "10": 10,
            "J" : 10,
            "Q" : 10, 
            "K" : 10,
            "A" : 11, 
            }
        suits = ["spade", "club", "heart", "diamond"]
        for i in range(self.decks):
            for s in suits:
                for v in valueMap:
                    c = Card(v, valueMap[v], s)
                    self.cards.append(c)
        
        for i in range(random.randint(2, 4)):
            random.shuffle(self.cards)
            
        
        

    
            
