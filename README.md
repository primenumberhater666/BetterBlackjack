# BetterBlackjack

BetterBlackjack is a web app designed for those who are interested in the numbers of card counting in blackjack.

This simulator allows the user to get a general idea of what their expected value (EV) looks like, based on their bet spread and table conditions. Support for other blackjack variants (i.e. S17 or dealer peek) has not yet been implemented.
With the variant available, users can compute the following data:

* Expected Value (EV) per round
* Average Win per Round
* Average Win per Hour
* Standard Deviation of one hour's play 
* Risk of Ruin (RoR) given a fixed bankroll

## Running the app
* After running \
`npm install` \
`npm run dev` \
Open another terminal and start the backend with `npm run api`

## Rules and Strategy

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

* Counting System
    - The simulator uses the Hi-Lo count system, where low value cards (2-6) add one to the count, while high value cards (10-A) subtract one from the count.
    - The rough estimate, is that for every increase in the true count, the player gains about a 0.5% edge over the casino. Obviously, this trend is not linear, and this is just an estimate.

* Strategy
    - The tracked player will play perfect basic strategy, while deviating based on the count.
    - The exact deviations that the player uses can be found in the `./react-with-flask/api/strategies` directory.
    - All other players at the table will play perfect basic strategy.

## Other Important Notes

* Anything under 10 million rounds can be incredibly inaccurate. The recommendation is to simulate as many rounds as your hardware allows in order to maximize accuracy.
You can change the number of simulations ran by modifying the `numSims` field in `./react-with-flask/src/components/SimSettings.tsx`.
* The option to late surrender gives the player an additional 0.08% edge when used correctly. This change will inevitably improve the stats of a double deck game slightly, 
    but note that you will likely never find a casino that offers a surrender double deck game. 