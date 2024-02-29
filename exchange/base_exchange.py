
# abstract class
class BaseExchange:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_order_book(self, coin):
        # get orderbook
        pass

    def get_ticker(self, coin, side=None):
        # get ticker
        pass

    def get_ohlcv(self, coin, since=None, limit=None, timeframe='1m'):
        # get ohlcv history
        pass

