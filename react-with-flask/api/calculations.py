import numpy as np

# returns profit per round 
def profitPerRound(total, rds):
    return total / rds 

# returns profit per hour
def profitPerHour(perRound, rph):
    return np.round(perRound * rph, decimals = 2)

# standard deviation (round)
def _stdev_per_round_numpy(deltas: list[float]) -> float:
    n = len(deltas)
    if n < 2:
        return 0.0
    return float(np.std(np.array(deltas, dtype=float), ddof=1))

# calculated total expected value (EV)
def _ev_percent_overall(profit: float, total_initial_wagered: float):
    if total_initial_wagered <= 0:
        return 0.0
    return 100.0 * (profit / total_initial_wagered)

# calculate expected value per round (EV)
def _ev_percent_per_round(profit_per_round: float, avg_initial_bet: float):
    if avg_initial_bet <= 0:
        return 0.0
    return 100.0 * (profit_per_round / avg_initial_bet)

# calculate RoR
def _risk_of_ruin_gaussian(starting_bankroll: float,mu_per_round: float, sigma_per_round: float):
    if sigma_per_round <= 0:
        if mu_per_round > 0:
            return 0.0
        else:
            return 1.0
    if mu_per_round <= 0:
        return 1.0
    expo = -2.0 * mu_per_round * starting_bankroll / (sigma_per_round ** 2)
    ror = float(np.exp(expo))

    if ror < 0.0:
        return 0.0
    elif ror > 1.0:
        return 1.0
    else:
        return ror