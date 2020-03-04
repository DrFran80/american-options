# -*- coding: utf-8 -*-

from calculator import (create_sample_matrix,
                        payoff_ifexercise,
                        paths_in_the_money,
                        stop_timesat_t,
                        )

from AmericanOption import AmericanPut

sample_matrix = create_sample_matrix( 1, 2, 0.02, 0.06, intervals = 100, samples =10)
put_option = AmericanPut( 1.10 )

prices =sample_matrix[:,-2]
    
payoff_at_T = payoff_ifexercise( sample_matrix[:,-1], put_option)

paths = paths_in_the_money( prices, put_option)
stop_times = stop_timesat_t( prices, payoff_at_T*0.943396, put_option)

#stop_time_matrix = np.column_stack((stop_times, stT))