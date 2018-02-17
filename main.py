import boto3
import json
import requests
from polling import poll_binance_data, poll_poloniex_data
from state_machine import FSM
from publish import push_notification
from exception import UnableToRetriveDataException
from enums import State, Sign


binance_poloniex_state_machine = FSM('binance', 'poloniex')


try:
    binance_data = poll_binance_data()
    poloniex_data = poll_poloniex_data()

    new_state, updated = binance_poloniex_state_machine.update_fsm(
                        {'bid_price': float(binance_data['bids'][0][0]), 'ask_price': float(binance_data['asks'][0][0])},
                        {'bid_price': float(poloniex_data['bids'][0][0]), 'ask_price': float(poloniex_data['asks'][0][0])}
                    )

    if updated:
        message_header = '[IMPORTANT] Bitcoin Price Updated' 
        if new_state == State.ZERO_PERCENTS:
            message_body = '%s price and %s price are back to equal, take action NOW!' % \
                binance_poloniex_state_machine.platform_1, binance_poloniex_state_machine.platform_2
        elif binance_poloniex_state_machine.sign == Sign.POSITIVE:
            message_body = '%s price is higher than %s price by %f%, take action NOW!' % \
                binance_poloniex_state_machine.platform_1, binance_poloniex_state_machine.platform_2, \
                float(new_state) * 100
        else:
            message_body = '%s price is higher than %s price by %f%, take action NOW!' % \
                binance_poloniex_state_machine.platform_2, binance_poloniex_state_machine.platform_1, \
                float(new_state) * 100

        push_notification(message_header, message_body)
    
#TODO: add other exce[tion] handling here
except UnableToRetriveDataException:
    print 'Error: unbale to retrive data through REST api'
    pass
