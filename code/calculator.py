# -*- coding: utf-8 -*-
import numpy as np
import math
import statsmodels.api as sm

def create_sample_path( spot_price, T, sigma, risk_free, intervals=10000):
    path = np.zeros(T*intervals+1)
    dt = 1 / intervals
    path[0] = spot_price
    drift = risk_free - 0.5*math.pow(sigma,2)
    shocks = np.random.normal(0, np.sqrt(dt), size = T * intervals + 1)
    for i in range(1, (T*intervals + 1)):
        path[i] = path[i-1] * np.exp( drift * dt + sigma * shocks[i])
    return path

def create_sample_matrix( spot_price, T, sigma, risk_free, intervals = 10000, samples = 1000):
    sample_matrix = np.zeros( (samples, T*intervals+1) )
    for i in range(samples):
        sample_matrix[i,:] = create_sample_path( spot_price, T, sigma, risk_free, intervals)
    return sample_matrix

def payoff_ifexercise( prices, claim ):
    return np.array([claim.payoff_ifexercise(p) for p in prices])

def filter_in_the_money( prices, claim):
    return np.array([ p if claim.payoff_ifexercise(p)> 0 else 0 for p in prices])

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

def stop_timeatT( prices, claim):
    return np.array([ bool(p) for p in filter_in_the_money(prices, claim) ], dtype =bool)

def stop_timesatK( prices_in_the_money, discounted_payoff, claim):
    X = prices_in_the_money[ prices_in_the_money > 0]
    y = discounted_payoff [prices_in_the_money > 0]
    X1 = sm.add_constant(X)
    EYX = sm.OLS(y,X1).fit().predict(X1)
    stop_times =  np.array( [ EYX[i] > claim.payoff_ifexercise(X[i]) for i in range(len(X))] )
    return extend_vector( prices_in_the_money, stop_times )

def discounted_payoff( payoff_matrix, risk_free ):
    if payoff_matrix.ndim == 1:
        return np.array( [p / (1+risk_free) for p in payoff_matrix ] )
    nrows, ncols = payoff_matrix.shape
    discounted_payoff = np.zeros(nrows)
    for i in range(ncols):
        discount_factor = (1+risk_free) ** ((-1)*(i+1))
        discounted_payoff += np.array([p * discount_factor for p in payoff_matrix[:,-i]])
    return discounted_payoff
 

    




