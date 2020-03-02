# -*- coding: utf-8 -*-
import numpy as np

def extend_vector( prices_in_the_money, stop_times ):
    st = np.zeros(len(prices_in_the_money), dtype=bool)
    j = 0
    for i in range(len(prices_in_the_money)):
        if prices_in_the_money[i]> 0 :
            st[i] = stop_times[j]
            j +=1
        else:
            st[i] = False
    return st