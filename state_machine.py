import boto3
import requests
import json
from enums import State, Sign
from utils import Utils


class FSM:
    def __init__(self, platform_1, platform_2, coin_type):
        self.platform_1 = platform_1
        self.platform_2 = platform_2
        self.coin_type = coin_type
        self.state = State.ZERO_PERCENTS
        self.name = platform_1 + "-" + platform_2
        self.diff = 0
        # sign: positive means platform_1 price higher than platform_2 price, 
        # You can buy from platform_2 and sell to platform_1
        self.sign = Sign.POSITIVE
        

    def update_fsm(self, platform_1_prices, platform_2_prices):
        updated = False

        #update diff
        self.diff = max(float(platform_1_prices['bid_price'] - platform_2_prices['ask_price'])\
                    /platform_2_prices['ask_price'],
                    float(platform_2_prices['bid_price'] - platform_1_prices['ask_price'])\
                    /platform_1_prices['ask_price'])


        if self.state == State.ZERO_PERCENTS:
            if float(platform_1_prices['bid_price'] - platform_2_prices['ask_price'])\
                    /platform_2_prices['ask_price'] >= 0.01:
                    self.sign = Sign.POSITIVE
                    self.state = 0.01
                    updated = True
            elif float(platform_2_prices['bid_price'] - platform_1_prices['ask_price'])\
                    /platform_1_prices['ask_price'] >= 0.01:
                    self.sign = Sign.NEGATIVE
                    self.state = 0.01
                    updated = True
        elif self.sign == Sign.POSITIVE:
            if float(platform_1_prices['bid_price'] - platform_2_prices['ask_price'])\
                    /platform_2_prices['ask_price'] >= self.state + Utils.interval:
                    self.state = self.state + Utils.interval
                    self.sign = Sign.POSITIVE
                    updated = True
            elif float(platform_1_prices['bid_price'] - platform_2_prices['ask_price'])\
                    /platform_2_prices['ask_price'] <= 0:
                    self.state = State.ZERO_PERCENTS
                    self.sign = Sign.POSITIVE
                    updated = True
        # self.sign == Sign.POSITIVE:
        else:
            if float(platform_2_prices['bid_price'] - platform_1_prices['ask_price'])\
                    /platform_1_prices['ask_price'] >= self.state + Utils.interval:
                    self.state = self.state + Utils.interval
                    self.sign = Sign.NEGATIVE
                    updated = True
            elif float(platform_2_prices['bid_price'] - platform_1_prices['ask_price'])\
                    /platform_2_prices['ask_price'] <= 0:
                    self.state = State.ZERO_PERCENTS
                    self.sign = Sign.POSITIVE
                    updated = True
                        
        return  self.state, updated


    def reset_fsm(self):
        self.state = State.ZERO_PERCENTS

