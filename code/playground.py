# -*- coding: utf-8 -*-

from calculator import (create_stop_time_matrix,
                        create_payoff_matrix,
                        discounted_payoff
                        )
from simulation import create_prices_matrix

from AmericanOption import AmericanPut
import numpy as np
#sample_matrix = create_sample_matrix( 1, 2, 0.02, 0.06, intervals = 100, samples =10)

#prices_matrix = np.array([(1.00,1.09,1.08,1.34),
#                         (1.00,1.16,1.26,1.54),
#                         (1.00,1.22,1.07,1.03),
#                         (1.00,0.93,0.97,0.92),
#                         (1.00,1.11,1.56,1.52),
#                         (1.00,0.76,0.77,0.90),
#                         (1.00,0.92,0.84,1.01),
#                         (1.00,0.88,1.22,1.34)])

prices_matrix = create_prices_matrix( 36, 1, 0.4, 0.06, intervals=10000, samples=1000)
put_option = AmericanPut( 40 )

#stop_times = create_stop_time_matrix( prices_matrix, put_option, .06)
#cash_flow_matrix = create_payoff_matrix(prices_matrix[:,1:], stop_times, put_option)
#payoff = discounted_payoff(cash_flow_matrix,0.06)
#value = np.average(payoff)