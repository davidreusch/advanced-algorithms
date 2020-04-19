import math
import random
from time import time
from statistics import mean

def medianindex(s):
    return len(s) // 2   # numeration starts with 0 so we can simply take the half rounded down as index

def trivial_median(s):
    # just sort and take the middle element
    s = sorted(s)
    return s[medianindex(s)]

def select(s,k,groupsize = 5):
    if len(s) < 30:
        # brute force
        s = sorted(s)
        return s[k]

    # create list of medians of 5-groups
    median_list = []
    for i in range(0, len(s), groupsize):
        median_list.append(trivial_median(s[i:i+groupsize]))


    # find median of list of medians
    q = select(median_list, medianindex(median_list))

    #partition list with median of medians as pivot
    s_smaller = [x for x in s if x < q]
    s_larger = [x for x in s if x > q]

    #recurse, as long as median is not found yet
    if len(s_smaller) > k:
        return select(s_smaller, k)
    elif len(s_smaller) == k:
        return q
    else:
        return select(s_larger, k - 1 - len(s_smaller))


def unique(liste):
    dic = {}
    res = []
    for i in range(len(liste)):
        if liste[i] not in dic:
            dic[liste[i]] = 0
            res.append(liste[i])
    return res

def generateList(n):
    liste = list(range(n*10))
    random.shuffle(liste)
    return liste[:n]

def test():
    def measure():
        liste = generateList(10000)
        start = time()
        median = select(liste,medianindex(liste),g)
        end = time()
        measure = ((end*1000)-(start*1000))
        return measure

    for g in range(5,100,2):
        values = []
        for i in range(100):
            values += [round(measure(),3)]
        avg = round(mean(values),3)
        print(g,avg)
        
test()
