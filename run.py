import boto3
import json
import requests
from polling import poll_data
from state_machine import FSM
from publish import push_notification
from exception import UnableToRetriveDataException
from enums import State, Sign
from time import sleep
import logging
import time
from utils import Utils
from  enums import CoinType
from writeDDB import put_item
from exception import AWSDDBException
from logs import Logs
import os

'''
This function runs the polling data, update state machine and notification process
'''
def run(state_machine):
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    logging.basicConfig(filename='logs/' + Logs.get_log_file_name(),level=logging.INFO)
    try:
        data_platform_1 = poll_data(coin_type=state_machine.coin_type, platform=state_machine.platform_1)
        data_platform_2 = poll_data(coin_type=state_machine.coin_type, platform=state_machine.platform_2)

        print {'bid_price': float(data_platform_1['bids'][0][0]), 'ask_price': float(data_platform_1['asks'][0][0])}, \
            {'bid_price': float(data_platform_2['bids'][0][0]), 'ask_price': float(data_platform_2['asks'][0][0])}
        logging.info({'bid_price': float(data_platform_1['bids'][0][0]), 'ask_price': float(data_platform_1['asks'][0][0])}, \
            {'bid_price': float(data_platform_2['bids'][0][0]), 'ask_price': float(data_platform_2['asks'][0][0])})
    
        new_state, updated = state_machine.update_fsm(
                            {'bid_price': float(data_platform_1['bids'][0][0]), 'ask_price': float(data_platform_1['asks'][0][0])},
                            {'bid_price': float(data_platform_2['bids'][0][0]), 'ask_price': float(data_platform_2['asks'][0][0])}
                        )
        
        if updated:
            message_header = '[IMPORTANT] %s Price Updated'  % state_machine.coin_type
            if new_state == State.ZERO_PERCENTS:
                message_body = state_machine.platform_1 + ' price and ' \
                    + state_machine.platform_2 + ' price are back to equal, take action NOW!'
            elif state_machine.sign == Sign.POSITIVE:
                message_body = state_machine.platform_1 + ' price is higher than ' \
                    + state_machine.platform_2 + ' price by ' \
                    + str(float(new_state) * 100) + '% take action NOW!' 
            else:
                message_body = state_machine.platform_2 + ' price is higher than ' \
                    + state_machine.platform_1 + ' price by ' \
                    + str(float(new_state) * 100) + '% take action NOW!' 

            push_notification(message_header, message_body)

    except UnableToRetriveDataException as e:
        print str(e) + e.message        
        print 'Error: unbale to retrive data through REST api'
        logging.error(str(e) + e.message)
        logging.error('Error: unbale to retrive data through REST api')
        pass
    except Exception as e:
        print str(e) + e.message
        logging.error(str(e) + e.message)
        pass