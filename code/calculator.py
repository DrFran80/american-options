# -*- coding: utf-8 -*-
import numpy as np
import math

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
    
sample_matrix = create_sample_matrix( 1, 2, 0.02, 0.06, intervals = 100, samples =10)


def call_price_payoff(spot_price, strike):
    return float( max( spot_price-strike, 0 ) )
    
def put_price_payoff(spot_price, strike):
    return float( max( strike-spot_price, 0 ) )
    
vect_call_price_payoff = np.vectorize(call_price_payoff)
vect_put_price_payoff = np.vectorize(put_price_payoff)

def payoff_ifexercise( prices, strike, isCall = False):
    return vect_call_price_payoff(prices, strike) if isCall else vect_put_price_payoff(prices, strike)
    
payoff_at_T = payoff_ifexercise( sample_matrix[:,-1], 1.1)

print (payoff_at_T)

def filter_in_the_money( prices, strike, call=False ):
    prices[ payoff_ifexercise( prices, strike)]

