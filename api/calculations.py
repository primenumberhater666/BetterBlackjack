import numpy as np

# returns profit per round 
def profitPerRound(total, rds):
    return total / rds 

# returns profit per hour
def profitPerHour(perRound, rph):
    return np.round(perRound * rph, decimals = 2)

def expectedValue():
    return

def stdDev(arr, time):
    return np.round(np.std(arr) / time, decimals = 2)

def n0():
    return

def riskOfRuin():
    return 