# BetterBlackjack

BetterBlackjack is a web app designed for those who are interested in the numbers of card counting in blackjack.





## Rules

The simulations are ran on the following hardcoded rules:

* Game Rules
    - Dealer hits soft 17 (H17)
    - No resplit aces - one card only (nRSA)
    - Double after split (DAS)
    - Double any first two cards (DA2)
    - Late Surrender is permitted in all circumstances (LS)
    - Insurance and even money permitted 
    - Split up to infinite hands (Note: The EV difference between infinite splits and 4 splits max is < 0.002%, and therefore was omitted in the design.)
    - European No Hole Card (ENHC) variant - Dealer does not take an upcard, but all non-original bets are refunded in the case of a dealer blackjack. (OBO)

* Strategy
    - The tracked player will play perfect basic strategy, while devaiating based on the count.
    - The exact deviations that the player uses can be found in the ./react-with-flask/api/strategies directory.
    - All other players at the table will play perfet basic strategy