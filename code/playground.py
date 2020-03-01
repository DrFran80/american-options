# -*- coding: utf-8 -*-

from calculator import *
from AmericanOption import AmericanPut

sample_matrix = create_sample_matrix( 1, 2, 0.02, 0.06, intervals = 100, samples =10)
put_option = AmericanPut( 1.15 )
    
payoff_at_T = payoff_ifexercise( sample_matrix[:,-1], put_option)

print(sample_matrix[:,-1])
print (payoff_at_T)

filterin = filter_in_the_money( sample_matrix[:,-2], put_option)
#
print(filterin)

EYX = cond_expec_byOLS( filterin, payoff_at_T)

print (EYX)

dp = discounted_payoff( EYX, 0.06)