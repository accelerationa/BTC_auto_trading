import boto3
import requests
import json
from exception import UnableToRetriveDataException
from maps import UrlMaps
from logs import Logs
import os
import logging



def poll_data(coin_type, platform):
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    logging.basicConfig(filename='logs/' + Logs.get_log_file_name(),level=logging.INFO)
    try:
        url = UrlMaps[platform][coin_type]
        response = requests.request("GET", url)
        json_data = json.loads(response.text)
    except KeyError:
        print 'Error: unexpected key'
        logging.error('Error: unexpected key')
        raise
    except:
        print 'Error: unable to retrive data from ' + platform
        raise UnableToRetriveDataException('Error: unable to retrive data from ' + platform)
    return json_data