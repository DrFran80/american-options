# -*- coding: utf-8 -*-
import numpy as np

def extend_vector( stop_times, paths_in_the_money ):
    st = np.zeros(len(paths_in_the_money), dtype=bool)
    j = 0
    for i in range(len(paths_in_the_money)):
        if paths_in_the_money[i] :
            st[i] = stop_times[j]
            j +=1
        else:
            st[i] = False
    return st