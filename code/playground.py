# -*- coding: utf-8 -*-

from calculator import *
from AmericanOption import AmericanPut

sample_matrix = create_sample_matrix( 1, 2, 0.02, 0.06, intervals = 100, samples =10)
put_option = AmericanPut( 1.15 )
    
payoff_at_T = payoff_ifexercise( sample_matrix[:,-1], put_option)

filterin = filter_in_the_money( sample_matrix[:,-2], put_option)
#
print(filterin)

stop_times = stop_timesatK( filterin, payoff_at_T, put_option)

print (stop_times)

stT = stop_timeatT( sample_matrix[:,-1], put_option)
print (stT)

stop_time_matrix = np.column_stack((stop_times, stT))