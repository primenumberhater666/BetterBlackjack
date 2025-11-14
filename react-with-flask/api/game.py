from hand import Hand
from shoe import Sequence 
from card import Card

from jsonreader import returnJson

class Game:
    def __init__(self, rem, seq, roll,  players, pos, twoHands):
        self.rem = rem   # number of hands remaining
        self.seq = seq   # current shoe status
        self.roll = roll # current bankroll
        self.strat = returnJson("bs_test.json")  # built in basic strategy
        self.dev = returnJson("bs_deviations_test.json")
        self.players = players # number of players at the table
        self.pos = pos   # position at the table. If there are n players at the table, the first player is pos = 0 and the dealer is pos = n. 
                         # Note: in the case that an extra hand is played, everyone gets shifted (i -> i + 1)
        self.hands = []
        self.twoHands = twoHands #true count to play two hands at
    
    # updates number of hands remaining
    def updateRemaining(self):
        self.rem -= 1

    # gets the dealers hand 
    # NOTE: This method must be changed in order to implement non-ENHC variants
    def getDealerHand(self):
        for h in self.hands:
            if h.dealer == True: 
                return h
            
    # upates the hands list to hold the current hands 
    def updateHands(self, currBet: int):
        # self.numSplits = 0 <--- infinite splits vs. max 4 splits improves player advantage by < 0.002%. Will be implemented at a later date. 
        # shuffles if cut card was already reached. If cut card is the next card to be dealt, continue play. 
        if self.seq.cardsRemaining() < 0:
            self.seq.shuffle()
        # player hands: 
        for i in range(self.players): 
            hand = None 
            if i == self.pos and currBet > 0: # wonging out == bet is zero 
                hand = Hand(currBet, False)
                hand.isTracked[0] = True   
                hand.isTracked[1] = True
                if self.seq.getTC() >= self.twoHands: # play two hands. 
                    handTwo = Hand(currBet, False)
                    handTwo.isTracked[0] = True   
                    handTwo.isTracked[1] = True 
                    handTwo.dealCards(self.seq) 
                    handTwo.dealCards(self.seq)
                    self.hands.append(handTwo)
            else: 
                hand = Hand(0, False)          # creates empty hand 
            hand.dealCards(self.seq)        # deal 2 cards from current Sequence to Hand
            hand.dealCards(self.seq) 
            self.hands.append(hand)
        
        # Create dealer hand 
        dealerHand = Hand(0, True)
        dealerHand.dealCards(self.seq)
        self.hands.append(dealerHand)

        for h in self.hands:
            self.makeChoice(h)

        self.checkOutcome(currBet) 
        self.updateRemaining() 
        self.hands.clear()

    # Checks the outcome of each hand. If the busted hand is the simmed player, deduct bankroll.
    def checkOutcome(self, bet: int):
        dealerHand = self.getDealerHand()
        dealerBlackjack = dealerHand.checkBlackjack()
        dealerVal = dealerHand.value

        for h in self.hands:
            if h.isTracked[0]:
                double = 2 * bet 
                if dealerBlackjack and h.isTracked[1]: #if dealer bj and hand is original bet
                    if h.isInsured: # if player buys insurance
                        if h.checkBlackjack(): # even money rule 
                            self.roll += (1.5 * bet) 
                        else:
                            self.roll += bet / 2 # basically refund insurance bet.
                            continue
                    if not h.checkBlackjack(): # if player does not also have blackjack
                        self.roll -= bet 
                    else:
                        continue 
                elif dealerBlackjack and not h.isTracked[1]: #if dealer has bj and hand is NOT original bet
                    continue
                elif h.surrendered: # if player surrenders and dealer has no bj
                    self.roll -= bet / 2 # lose half of bet 
                else:
                    if h.checkBlackjack():
                        self.roll += (bet * 1.5)
                        # print(f"paid {(bet * 1.5)} for player BJ")
                        continue
                    if h.isDoubled:
                        if h.value > 21: # if player busts
                            self.roll -= double # lose the double

                        elif h.value > dealerVal or dealerVal > 21: # if player beats dealer
                            self.roll += double 

                        elif h.value < dealerVal and dealerVal <= 21: # if player loses to dealer
                            self.roll -= double 
                        else: 
                            continue 
                    else:
                        if h.value > 21: # if player busts
                            self.roll -= bet # lose the bet

                        elif h.value > dealerVal or dealerVal > 21: # if player beats dealer
                            self.roll += bet 

                        elif h.value < dealerVal and dealerVal <= 21: # if player loses to dealer
                            self.roll -= bet 
                        else: 
                            continue 

    # makes the correct choice based on player's hand, dealers upcard, 
    # basic strategy, and user-loaded deviations 
    def makeChoice(self, hand):
        if hand.dealer:
            while hand.value < 17 or (hand.value == 17 and hand.isSoft): #dealer hits soft 17 
                hand.dealCards(self.seq)
                hand.calculateScore()
            return

        # if not tracked player, play basic strategy
        if not hand.isTracked[0]:
            self.play(hand)
            return


        while True:
            # stop if bust
            if hand.value > 21:
                break

            key = self.toString(hand)
            true_count = self.seq.getTC()

            # insurance 
            if not (hand.isInsured or hand.isTracked[1]):
                insCutoff = self.dev["insurance"]["cutoff"]
                insOp = self.dev["insurance"]["op"]
                if decisionOperation(insOp, true_count, insCutoff) and self.getDealerHand().hand[0].symbol == "A":
                    self.takeInsurance(hand)

            play = None
            for d in self.dev["deviations"]:
                if d["key"] != key:
                    continue
                if decisionOperation(d["op"], true_count, d["cutoff"]):
                    play = d["action"]
                    break
            # no deviation: basic strategy
            if play is None:
                play = self.strat["basic_strategy"][key]

            if play == "R":  # surrender
                hand.surrendered = True
                break

            if play == "S":  # stand
                break

            if play == "P":  # split
                newHand = Hand(hand.bet, False)
                newHand.isTracked[0] = True 
                self.hands.insert(self.hands.index(hand) + 1, newHand)
                newHand.hand.append(hand.hand.pop(1))

                if hand.hand[0].value == 11:  # no resplit aces
                    newHand.dealCards(self.seq)
                    hand.value /= 2
                    hand.dealCards(self.seq)
                    break
                newHand.dealCards(self.seq)
                hand.value /= 2
                hand.dealCards(self.seq)
                break
            if play == "D":  # double
                hand.dealCards(self.seq)
                hand.isDoubled = True
                break
            if play == "H":  # hit
                hand.dealCards(self.seq)
                continue
        return
        
    def play(self, hand):
        while True:
            h = self.toString(hand)
            if hand.value > 21:
                break 
            play = self.strat["basic_strategy"][h]
            if play == "R": # surrender
                hand.isSurrendered = True 
                break
            if play == "S":
                break
            if play == "P":
                newHand = Hand(hand.bet, False) # split hand
                self.hands.insert(self.hands.index(hand) + 1, newHand)
                newHand.hand.append(hand.hand.pop(1)) # moves card from hand to newHand
                if hand.hand[0].value == 11:          # No resplit aces 
                    newHand.dealCards(self.seq)
                    hand.value /= 2 # halves the value after split
                    hand.dealCards(self.seq)
                    break
                newHand.dealCards(self.seq)
                hand.value /= 2 # halves the value after split
                hand.dealCards(self.seq)
            if play == "D":  # double 
                hand.dealCards(self.seq)
                hand.isDoubled = True 
                break
            if play == "H":
                hand.dealCards(self.seq) # hit

        return 
    # Take insurance for a hand.
    def takeInsurance(self, hand):
        self.roll -= hand.bet / 2 
        hand.isInsured = True 

    # return string representation for decisions with dealer upcard
    # Example format hard 16 against ace: hard:16|A
    def toString(self, hand):
        dealerCard = self.getDealerHand().hand[0].value 
        if dealerCard == 10:
            dealerCard = "T"
        if dealerCard == 11:
            dealerCard = "A"
        
        id = "hard"
        if hand.isPair():
            id = "pair"
            return id + ":" + str(int(hand.value / 2)) + "|" + str(dealerCard)
        elif hand.isSoft:
            id = "soft"

        return id + ":" + str(int(hand.value)) + "|" + str(dealerCard)


    # Returns true if number of hands has been exhausted
    def isGameEnded(self):
        return self.rem <= 0

# takes in the string operations below:
# op: < > == <= >= 
# and returns a op b
# op must be one of the operations above 
def decisionOperation(op: str, a, b):
    if op == "<":
        return a < b
    if op == ">":
        return a > b
    if op == "==":
        return a == b 
    if op == "<=":
        return a <= b 
    if op == ">=":
        return a >= b 