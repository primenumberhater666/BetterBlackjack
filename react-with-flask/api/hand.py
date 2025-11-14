import numpy as np
import random
from random import randint 
from shoe import Sequence
from card import Card


class Hand:
    def __init__(self, bet:int, dealer: bool):
        self.hand = [] # List of Card 
        self.bet = bet 
        self.value = 0           
        self.aces = 0
        self.surrendered = False        # has hand been surrendered?
        self.isTracked = [False, False] # Index 0: Is the hand tracked? Index 1: is this the original hand?
        self.isDoubled = False          # Has the hand been doubled down? 
        self.isInsured = False          # is Hand insured?
        self.isSoft = False             # is Hand a soft hand? 
        self.dealer = dealer            # is Hand the dealer hand? 
        self.hiddenCard = None          # implementation for dealer peeking in the future

    # deal card to hand object.
    # consumes a sequence and modifies self 
    def dealCards(self, seq: Sequence):
        card = seq.cards[seq.curr]
        self.hand.append(card)
        self.calculateScore()
        seq.updateRC()
        seq.getNextCard()

    # return true iff players first two cards is a pair.
    # REQUIRES: Hand must contain two cards exactly. 
    def isPair(self):
        return len(self.hand) == 2 and self.hand[0].value == self.hand[1].value


    # splits a hand by producing a new one. 
        
    # Returns true if hand is a blackjack.
    # blackjack occurs iff their first two cards is an A and T in some order.
    def checkBlackjack(self):
        return len(self.hand) == 2 and self.value == 21 

        
    # Calculates the score for a particular hand
    def calculateScore(self):
        total = 0 
        aces = 0
        for c in self.hand:
            total += c.value
            if c.value == 11: aces += 1
        
        while aces > 0 and total > 21:
            total -= 10 
            aces -= 1

        if aces == 0: 
            self.isSoft = False
        else:
            self.isSoft = True 
        
        self.value = total

    # testing method, delete later!
    def __str__(self):
        for c in self.hand:
            print(c)
        