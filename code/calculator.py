# -*- coding: utf-8 -*-
from lib import extend_vector
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

def payoff_ifexercise( prices_atT, claim ):
    '''The payoff of the claim of a set of prices at time t'''
    return np.array([claim.payoff_ifexercise(p) for p in prices_atT])

def paths_in_the_money( prices_atT, claim):
    '''  True if the claim value is positive, else False'''
    return np.array([ claim.payoff_ifexercise(p)> 0 for p in prices_atT ], dtype =bool)

def stop_timesat_t( prices_atT, discounted_payoff, claim):
    ''' Receives a vector of prices at time t only if they are in 
    '''
    paths = paths_in_the_money( prices_atT, claim) 
    X = np.array( [ p for i,p in enumerate(prices_atT) if paths[i] ] )
    y = np.array( [ dp for i,dp in enumerate(discounted_payoff) if paths[i] ] )
    X1 = sm.add_constant(X)
    EYX = sm.OLS(y,X1).fit().predict(X1)
    stop_times =  np.array( [ claim.payoff_ifexercise(X[i]) > EYX[i] for i in range(len(X))] )
    return extend_vector(stop_times, paths)

def discounted_payoff( payoff_matrix, risk_free ):
    if payoff_matrix.ndim == 1:
        return np.array( [p / (1+risk_free) for p in payoff_matrix ] )
    nrows, ncols = payoff_matrix.shape
    discounted_payoff = np.zeros(nrows)
    for i in range(ncols):
        discount_factor = (1+risk_free) ** ((-1)*(i+1))
        discounted_payoff += np.array([p * discount_factor for p in payoff_matrix[:,-i]])
    return discounted_payoff
 





