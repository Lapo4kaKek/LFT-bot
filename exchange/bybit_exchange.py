from .base_exchange import BaseExchange
import ccxt
import ccxt.async_support as ccxt
from pybit.unified_trading import HTTP


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
        self.session = HTTP(
            testnet=False,
            api_key=self.api_key,
            api_secret=self.api_secret,
        )

    def get_order_book(self, coin, limit=None):
        return super().get_order_book(coin, limit)

    def get_ohlcv(self, coin, since=None, limit=None, timeframe='1m'):
        return super().get_ohlcv(coin, since, limit, timeframe)

    async def get_ticker(self, coin, side=None):
        return await super().get_ticker(coin, side)

    # you need add a parameters checker
    async def create_order(self, coin, type, side, amount, price, params=None):
        if params is None:
            params = {}
        return await super().create_order(coin, type, side, amount, price, params)

    def get_balance(self):
        return super().get_balance()

    # futures
    def set_leverage(self, coin, level):
        """

        :param coin: Example: SOL/USDT = SOLUSDT
        :param level:
        :return:
        """
        return self.exchange.set_leverage(level, coin)

    # async def create_market_buy_order(self, symbol, order_size):
    #     return await super().create_market_buy_order(symbol, order_size)
    #
    # async def create_market_sell_order(self, symbol, order_size):
    #     return await super().create_market_sell_order(symbol, order_size)
    async def create_market_buy_order_with_cost(self, coin, cost, params=None):
        if params is None:
            params = {}
        return await self.exchange.create_market_buy_order_with_cost(coin,
                                                                     cost, params)

    async def create_market_sell_order_with_cost(self, coin, cost):
        return await self.exchange.create_market_sell_order_with_cost(coin,
                                                                      cost)

    def get_order_history(self, limit=5):
        result = self.session.get_order_history(
            category="linear",
            limit=limit,
        )
        return result

    def get_trade_history(self, limit=9999):
        result = self.session.get_executions(
            category="linear",
            limit=1,
        )
        return result

    def find_order_by_id(self, order_id):
        order_history = self.get_trade_history()
        for order in order_history['result']['list']:
            if order['orderId'] == order_id:
                return order
        return None
