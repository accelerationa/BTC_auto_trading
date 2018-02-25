
import datetime
import time

class Utils:
    interval = 0.005
    time_interval = 10 #time intervals for every two writing DDB, in seconds
    sleep_time = 5 #time intervals between each two polling from trading platform
    Poloniex = 'poloniex'
    Binance = 'binance'

    @staticmethod
    def get_PST_time():
        timestamp = int(time.time())

        t = datetime.datetime.fromtimestamp(
            int(timestamp)
        ).strftime('%Y-%m-%d %H:%M:%S')
        return t