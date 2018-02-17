import boto3
import requests
import json
from exception import UnableToRetriveDataException


def poll_binance_data():
    try:
        url = "https://www.binance.com/api/v1/depth?limit=10&symbol=BTCUSDT"
        response = requests.request("GET", url)
        json_data = json.loads(response.text)
    except:
        print 'Error: unable to retrive data from Binance'
        raise UnableToRetriveDataException()
    return json_data


def poll_poloniex_data():
    try:
        url = "https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_BTC&depth=10"
        response = requests.request("GET", url)
        json_data = json.loads(response.text)
    except:
        print 'Error: unable to retrive data from Poloniex'
        raise UnableToRetriveDataException()
    return json_data