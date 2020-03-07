# -*- coding: utf-8 -*-
from lib import extend_vector
import numpy as np
from sklearn.linear_model import LinearRegression

def payoff_ifexercise( prices_atT, claim ):
    '''The payoff of the claim of a set of prices at time t'''
    return np.array([claim.payoff_ifexercise(p) for p in prices_atT])

def paths_in_the_money( prices_atT, claim):
    '''  True if the claim value is positive, else False'''
    st = np.array([ claim.payoff_ifexercise(p)> 0 for p in prices_atT ], dtype =bool)
    return np.reshape(st,(st.size,1))

def create_X_data(prices_atT,paths):
    X1 = np.array( [ p for i,p in enumerate(prices_atT) if paths[i] ] )
    X2 = X1 ** 2
    return np.column_stack((np.ones_like(X1), X1,X2))

def stop_timesat_t( prices_atT, discounted_payoff, claim):
    ''' Receives a vector of stop times at  t 
    '''
    paths = paths_in_the_money( prices_atT, claim).flatten() 
    X = create_X_data(prices_atT,paths)
    y = np.array( [ dp for i,dp in enumerate(discounted_payoff) if paths[i] ] )
    model = LinearRegression().fit(X,y)
    EYX = model.predict(X).flatten()
    stop_times =  np.array( [ claim.payoff_ifexercise(X[i,1]) > EYX[i] for i in range(X.shape[0])] )
    return extend_vector(stop_times, paths)

def discounted_payoff( payoff_matrix, risk_free ):
    '''Returns a vector of the of discounted payoff from t to T 
        ( discounted according to where they are in time)
    '''
    nrows, ncols = payoff_matrix.shape
    discounted_payoff = np.zeros(nrows)
    for i in range(ncols):
        discount_factor = (1+risk_free) ** ((-1)*(ncols-i))
        discounted_payoff += np.array([p * discount_factor for p in payoff_matrix[:,(ncols-i-1)]])
    return discounted_payoff

def create_payoff_matrix( prices_matrix, partial_stop_times, claim):
    '''Given a prices_matrix and a matrix of stop times from t+1 to T, returns the
        payoff matrix from t+1 to T
    '''
    payoff_matrix = np.zeros_like(prices_matrix, dtype = float)
    nrows, ncols = prices_matrix.shape
    for i in range(nrows):
        for j in range(ncols):
            payoff_matrix[i,j] = claim.payoff_ifexercise(prices_matrix[i,j]) if partial_stop_times[i,j] else 0
    return payoff_matrix

def clean_stop_time_matrix(partial_stop_times, stop_times_at_t):
    ''' Given a partial stop times matrix from t+1 to T and the stop times at t,
        returns the new stop times matrix from t to T
    '''
    new_partial_stop_times = np.empty_like( partial_stop_times, dtype = bool )                             
    for i in range(len(stop_times_at_t)):
        if stop_times_at_t[i]:
            new_partial_stop_times[i,:] = np.zeros_like(partial_stop_times[i,:], dtype = bool )
        else:
            new_partial_stop_times[i,:] = partial_stop_times[i,:] 
    return np.column_stack(( stop_times_at_t,new_partial_stop_times ))
        
 
def create_stop_time_matrix( prices_matrix, claim, risk_free, steps):
    _, ncols = prices_matrix.shape
    step_risk_free = ( (1 + risk_free) ** (1/steps) ) - 1
    for t in range(1,ncols): 
        if t == 1:
            partial_stop_times = paths_in_the_money (prices_matrix[:,-t], claim)
        else:
            payoff_matrix = create_payoff_matrix (prices_matrix[:,-(t-1):], partial_stop_times, claim)
            d_payoff = discounted_payoff( payoff_matrix, step_risk_free )
            stop_times_at_t = stop_timesat_t( prices_matrix[:,-t], d_payoff, claim)
            partial_stop_times = clean_stop_time_matrix(partial_stop_times, stop_times_at_t)
    return partial_stop_times
        
        





