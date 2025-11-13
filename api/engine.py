
from game import Game 
from shoe import Sequence
from calculations import *

def run(
    num_sims: int,
    starting_bankroll: int,
    decks_used: int,
    penetration_cards: int,
    spread: list[dict],
    players: int,
    two_hands_tc: int,
    rounds_per_hour: int
):
    seq = Sequence(decks_used, penetration_cards)
    seq.shuffle()

    gm = Game(num_sims, seq, starting_bankroll, players, 0, two_hands_tc)

    spread_by_tc = {row["count"]: row["bet"] for row in spread}
    while not gm.isGameEnded():
        tc = int(seq.getTC())
        if tc <= -2:
            countKey = -2
        if tc >= 7:
            countKey = 7
        if -1 <= tc <= 7:
            countKey = tc
            bet = spread_by_tc.get(countKey, 0)
        gm.updateHands(bet)

    profit = gm.roll - starting_bankroll
    profit_per_round = profitPerRound(profit, num_sims)    
    profit_per_hour = profitPerHour(profit_per_round, rounds_per_hour)        
    # stdev_per_hour = stdDev(np_bankroll, num_sims / rounds_per_hour)

    return {
        "hands_played": num_sims,
        "final_bankroll": gm.roll,
        "profit": profit,
        "profit_per_round": profit_per_round,
        "profit_per_hour":  profit_per_hour,
        "stdev_per_hour":   0,
    }
