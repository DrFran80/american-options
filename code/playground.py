# -*- coding: utf-8 -*-

from calculator import (create_sample_matrix,
                        payoff_ifexercise,
                        filter_in_the_money,
                        stop_timesat_t,
                        stop_timeatT)

from AmericanOption import AmericanPut
import numpy as np

sample_matrix = create_sample_matrix( 1, 2, 0.02, 0.06, intervals = 100, samples =10)
put_option = AmericanPut( 1.15 )
    
payoff_at_T = payoff_ifexercise( sample_matrix[:,-1], put_option)

filterin = filter_in_the_money( sample_matrix[:,-2], put_option)
stop_times = stop_timesat_t( filterin, payoff_at_T, put_option)

stT = stop_timeatT( sample_matrix[:,-1], put_option)

stop_time_matrix = np.column_stack((stop_times, stT))