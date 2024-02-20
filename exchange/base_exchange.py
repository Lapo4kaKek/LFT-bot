
# abstract class
class BaseExchange:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_order_book(self):
        # get orderbook
        pass

    def calculate_order_cost(self, symbol, amount, side):
        # get order cost
        pass

    def get_ohlcv(self, symbol, timeframe, since, limit):
        # get ohlcv history
        pass

