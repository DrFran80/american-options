# -*- coding: utf-8 -*-
from Claim import Claim

class AmericanOption( Claim ):
    def __init__(self, strike, maturity = 1, underlying=None):
        self.strike = strike
        self.maturity = maturity
        self.underlying = underlying
    
    def payoff_ifexercise( self, spot_price ):
        pass
    
class AmericanCall( AmericanOption ):
    def payoff_ifexercise( self, spot_price ):
        return float( max( spot_price-self.strike, 0 ) )

class AmericanPut( AmericanOption ):
    def payoff_ifexercise( self, spot_price):
        return float( max( self.strike-spot_price, 0 ) )