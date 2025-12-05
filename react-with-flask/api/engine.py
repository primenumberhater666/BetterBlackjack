
from game import Game
from shoe import Sequence
import numpy as np
from calculations import * 
from math import sqrt
from calculations import _stdev_per_round_numpy, _ev_percent_overall, _ev_percent_per_round, _risk_of_ruin_gaussian

# tc operations
def _clamp_tc(tc):
    if tc <= -2:
        return -2
    elif tc >= 7:
        return 7
    else:
        return tc


# run the simulation
def run(num_sims: int,
        starting_bankroll: int,
        decks_used: int,
        penetration_cards: int,
        spread: list[dict],    
        players: int,
        two_hands_tc: int,
        rounds_per_hour: int):
    
    # Shoe and game initialization
    seq = Sequence(decks_used, penetration_cards)
    seq.shuffle()
    gm = Game(num_sims, seq, starting_bankroll, players, 0, two_hands_tc)

    # TC to Bet correspondence
    spread_by_tc = {int(row["count"]): int(row["bet"]) for row in spread}

    bankroll_series = []           # bankroll after each round
    round_deltas = []              # bankroll change each round
    total_initial_wagered = 0.0    
    rounds_with_bet = 0           

    # simulator loop
    while not gm.isGameEnded():
        tc_int = int(seq.getTC())
        key = _clamp_tc(tc_int)
        bet = int(spread_by_tc.get(key, 0))

        before = gm.roll
        gm.updateHands(bet)
        after = gm.roll

        # collect stats
        round_deltas.append(after - before)
        bankroll_series.append(after)

        if bet > 0:
            total_initial_wagered += bet
            rounds_with_bet += 1

    # important data 
    profit = gm.roll - starting_bankroll
    profit_per_round_val = profitPerRound(profit, num_sims)
    profit_per_hour_val = profitPerHour(profit_per_round_val, rounds_per_hour)

    # standard deviation
    stdev_per_round = _stdev_per_round_numpy(round_deltas)
    stdev_per_hour = stdev_per_round * sqrt(max(rounds_per_hour, 0))

    if rounds_with_bet > 0:
        avg_initial_bet = (total_initial_wagered / rounds_with_bet)
    else:
        avg_initial_bet = 0.0

    ev_overall_pct  = _ev_percent_overall(profit, total_initial_wagered)
    ev_pr_pct = _ev_percent_per_round(profit_per_round_val, avg_initial_bet)

    mu_per_round = profitPerRound(profit, num_sims)
    sigma_per_round = _stdev_per_round_numpy(round_deltas)
    risk_of_ruin = _risk_of_ruin_gaussian(starting_bankroll=float(starting_bankroll),
                                          mu_per_round=float(mu_per_round),
                                          sigma_per_round=float(sigma_per_round))
    
    risk_of_ruin *= 100 # convert to %
    profit_per_round_val = np.round(profit_per_hour_val, decimals = 2)
    stdev_per_hour = np.round(stdev_per_hour, decimals = 2)
    ev_overall_pct = np.round(ev_pr_pct, decimals = 3)
    ev_pr_pct = np.round(ev_pr_pct, decimals = 3)
    stdev_per_hour = np.round(stdev_per_hour, decimals = 2)
    risk_of_ruin = np.round(risk_of_ruin, decimals = 4)

    return {
        "hands_played": num_sims,
        "final_bankroll": gm.roll,
        "profit": profit,
        "profit_per_round": profit_per_round_val,
        "profit_per_hour": profit_per_hour_val,
        "stdev_per_hour": stdev_per_hour,
        "ev_overall_percent": ev_overall_pct,     
        "ev_per_round_percent": ev_pr_pct,        
        "risk_of_ruin": risk_of_ruin,
    }
