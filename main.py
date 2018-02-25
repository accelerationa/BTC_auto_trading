import boto3
import json
import requests
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
from run import run
import os
from logs import Logs


binance_poloniex_state_machine = FSM(Utils.Binance, Utils.Poloniex, CoinType.BTC)


def main():
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    logging.basicConfig(filename='logs/' + Logs.get_log_file_name(),level=logging.INFO)

    start_time = int(time.time())
    max_diff = init_max_diff_dict()


    while True:
        try:
            logging.info(Utils.get_PST_time())

            if int(time.time()) - start_time >= Utils.time_interval:
                #write the table
                put_item(coin_type=binance_poloniex_state_machine.coin_type, \
                    compare_type=binance_poloniex_state_machine.platform_1+'-'+binance_poloniex_state_machine.platform_2,\
                    diff=str(max_diff), start=start_time, end=int(time.time()))
                start_time = int(time.time())
                max_diff = reset_max_diff_dict()

            run(binance_poloniex_state_machine)



            max_diff[binance_poloniex_state_machine.name] = max(max_diff[binance_poloniex_state_machine.name], \
                binance_poloniex_state_machine.diff)

            print "max_diff: "
            print max_diff
            logging.info("max_diff: ")
            logging.info(max_diff)
            

        except AWSDDBException as e:
            print str(e) + e.message
            logging.error(str(e) + e.message)            
            start_time = int(time.time())
            max_diff = reset_max_diff_dict()
            pass
        except Exception as e:
            print str(e) + e.message
            logging.error(str(e) + e.message)
            print 'Runtime error happend in main'
            logging.error('Runtime error happend in main')
            pass

        print "\n\n"
        logging.info('\n\n')

        sleep(Utils.sleep_time)
        

def init_max_diff_dict():
    max_diff = {
        binance_poloniex_state_machine.name: 0
    }
    return max_diff

def reset_max_diff_dict():
    return init_max_diff_dict()
    

if __name__ == "__main__":
    main()