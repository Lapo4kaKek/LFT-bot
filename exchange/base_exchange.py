from abc import ABC, abstractmethod
import ccxt.async_support as ccxt


class BaseExchange(ABC):
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
        })

    @abstractmethod
    def get_order_book(self, coin, limit=None):
        return self.exchange.fetch_order_book(coin, limit)

    @abstractmethod
    async def get_ticker(self, coin, side=None):
        ticker = await self.exchange.fetch_ticker(coin)
        if side == 'buy':
            return ticker["ask"], ticker["askVolume"]
        elif side == 'sell':
            return ticker["bid"], ticker["bidVolume"]
        return ticker

    @abstractmethod
    def get_ohlcv(self, coin, since=None, limit=None, timeframe='1m'):
        params = {}
        if since is not None:
            params['since'] = since
        if limit is not None:
            params['limit'] = limit

        return self.exchange.fetch_ohlcv(coin, timeframe, **params)

    @abstractmethod
    async def create_order(self, coin, type, side, amount, price=None, params={}):
        """
        :param coin: Token name
        :param type: Market or Limit
        :param amount: Buy or Sell
        :param price:
        :return: order_id?
        """
        return await self.exchange.create_order(coin, type, side, amount, price, params)

    @abstractmethod
    async def get_balance(self):
        return await self.exchange.fetch_balance()

    # futures
    def update_leverage(self, coin, level):
        pass

    async def cancel_order(self, order_id, symbol):
        pass

    async def fetch_order(self, order_id, symbol):
        pass

    async def create_market_buy_order(self, strategy_id, symbol, order_size):
        return await self.exchange.create_order(symbol, 'market', 'buy', order_size)

    async def create_market_sell_order(self, strategy_id, symbol, order_size):
        return await self.exchange.create_order(symbol, 'market', 'sell', order_size)