import math

def fastpot(a,n):
    """calculate n-th pot of a"""
    power = a
    logbound = math.floor(math.log2(n))
    for i in range(logbound):
        power = power * power
    for j in range(n - 2 ** logbound):
        power = power * a

    return power


