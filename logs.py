
import datetime
import time

class Logs:
    LOG_TIME_INTERVAL = 3600*4
    @staticmethod
    def get_log_file_name():
        timestamp = int(time.time()) - int(time.time()) % (Logs.LOG_TIME_INTERVAL)

        t = datetime.datetime.fromtimestamp(
            int(timestamp)
        ).strftime('%Y-%m-%d %H:%M:%S')
        return str(t)