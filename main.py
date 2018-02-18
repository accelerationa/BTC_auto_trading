import boto3
import json
import requests
from polling import poll_binance_data, poll_poloniex_data
from state_machine import FSM
from publish import push_notification
from exception import UnableToRetriveDataException
from enums import State, Sign
from time import sleep
import logging
import time


def main():
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.info('Started execution from MAIN')

    binance_poloniex_state_machine = FSM('binance', 'poloniex')


    while True:
        try:
            logger.info('Time:' + str(time.time()))            
            binance_data = poll_binance_data()
            poloniex_data = poll_poloniex_data()
            
            #for test
            print 'In main.py, prices are: '
            print {'bid_price': float(binance_data['bids'][0][0]), 'ask_price': float(binance_data['asks'][0][0])}, {'bid_price': float(poloniex_data['bids'][0][0]), 'ask_price': float(poloniex_data['asks'][0][0])}
            logger.info('In main.py, prices are: ')            
            logger.info({'bid_price': float(binance_data['bids'][0][0]), 'ask_price': float(binance_data['asks'][0][0])})            
            logger.info({'bid_price': float(poloniex_data['bids'][0][0]), 'ask_price': float(poloniex_data['asks'][0][0])})            
            
       
            new_state, updated = binance_poloniex_state_machine.update_fsm(
                                {'bid_price': float(binance_data['bids'][0][0]), 'ask_price': float(binance_data['asks'][0][0])},
                                {'bid_price': float(poloniex_data['bids'][0][0]), 'ask_price': float(poloniex_data['asks'][0][0])}
                            )

            logger.info('Updated: ' + str(updated))
            logger.info('New state: ' + str(binance_poloniex_state_machine.state))            
            if updated:
                message_header = '[IMPORTANT] Bitcoin Price Updated' 
                if new_state == State.ZERO_PERCENTS:
                    message_body = binance_poloniex_state_machine.platform_1 + ' price and ' \
                        + binance_poloniex_state_machine.platform_2 + ' price are back to equal, take action NOW!'
                elif binance_poloniex_state_machine.sign == Sign.POSITIVE:
                    message_body = binance_poloniex_state_machine.platform_1 + ' price is higher than ' \
                        + binance_poloniex_state_machine.platform_2 + ' price by ' \
                        + str(float(new_state) * 100) + '% take action NOW!' 
                else:
                    message_body = binance_poloniex_state_machine.platform_2 + ' price is higher than ' \
                        + binance_poloniex_state_machine.platform_1 + ' price by ' \
                        + str(float(new_state) * 100) + '% take action NOW!' 

                logger.info('pushing notification.')                            
                push_notification(message_header, message_body)

        #TODO: add other exce[tion] handling here
        except UnableToRetriveDataException:
            print 'Error: unbale to retrive data through REST api'
            logger.error('unbale to retrive data through REST api')
            pass
        except:
            print 'Runtime error happend'
            logger.error('Runtime error happend')
            pass
        
        print '\n\n\n'
        sleep(30)


if __name__ == "__main__":
    logging.info("Begin")
    main()