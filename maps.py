from utils import Utils
from enums import CoinType

UrlMaps = {
    Utils.Binance: {
        CoinType.BTC: "https://www.binance.com/api/v1/depth?limit=10&symbol=BTCUSDT"
    },
    Utils.Poloniex: {
        CoinType.BTC: "https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_BTC&depth=10"
    }
}