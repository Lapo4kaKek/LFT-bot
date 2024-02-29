from .base_exchange import BaseExchange
import ccxt

class BybitExchange(BaseExchange):
    def __init__(self, api_key, api_secret):
        """
        Инициализирует экземпляр BinanceExchange с использованием предоставленных API key и API secret.
        :param api_key: API ключ пользователя для доступа к Binance.
        :param api_secret: Секретный ключ пользователя для доступа к Binance.
        """
        super().__init__(api_key, api_secret)
        self.exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret,
        })

    def get_order_book(self, coin, limit = None):
        return super().get_order_book(coin, limit)

    def get_ohlcv(self, coin, since=None, limit=None, timeframe='1m'):
        return super().get_ohlcv(coin, since, limit, timeframe)

    def get_ticker(self, coin, side=None):
        return super().get_ticker(coin, side)

    # you need add a parameters checker
    def create_order(self, coin, type, side, amount, price):
        return super().create_order(coin, type, side, amount, price)

