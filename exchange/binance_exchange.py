import ccxt
from .base_exchange import BaseExchange

class BinanceExchange(BaseExchange):
    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
        })

    def get_order_book(self, symbol):

        return self.exchange.fetch_order_book(symbol)

    def calculate_order_cost(self, symbol, amount, side):
        order_book = self.get_order_book(symbol)
        top_of_book = order_book['bids' if side == 'buy' else 'asks'][0]
        price = top_of_book[0]
        cost = price * amount
        return cost

    def aboba(self):
        pass
