
# abstract class
class BaseExchange:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_order_book(self):
        # get orderbook
        pass

    def get_ticker(self, symbol, side=None):
        # get ticker
        pass

    def get_ohlcv(self, symbol, timeframe, since, limit):
        # get ohlcv history
        pass

