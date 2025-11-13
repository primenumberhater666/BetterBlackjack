
# A very simple implementation of a playing card

class Card:
    def __init__(self, symbol, value, suit):
        self.symbol = str(symbol)
        self.value = value
        self.suit = suit
        
    # testing method, delete later!
    def __str__(self):
        return f"{self.symbol} of {self.suit}"

