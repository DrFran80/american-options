# -*- coding: utf-8 -*-
import numpy as np

def create_price_path( spot_price, T, sigma, risk_free, intervals=1000):
    path = np.zeros(T*intervals+1)
    dt = 1 / intervals * T
    path[0] = spot_price
    drift = risk_free - 0.5 * (sigma ** 2)
    shocks = np.random.normal(0, np.sqrt(dt), size = T * intervals + 1)
    for i in range(1, (T*intervals + 1)):
        path[i] = path[i-1] * np.exp( drift * dt + sigma * shocks[i])
    return path

def create_prices_matrix( S, T, sigma, risk_free, intervals = 10000, samples = 1000):
    sample_matrix = np.zeros( (samples, T*intervals+1) )
    for i in range(samples):
        sample_matrix[i,:] = create_price_path( S, T, sigma, risk_free, intervals)
    return sample_matrix