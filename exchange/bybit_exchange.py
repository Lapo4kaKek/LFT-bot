from .base_exchange import BaseExchange
import ccxt.async_support as ccxt
from pybit.unified_trading import HTTP
from utils.converter import Converter
from datetime import datetime


class BybitExchange(BaseExchange):
    def __init__(self, api_key, api_secret, monitoring):
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
        self.monitoring = monitoring

    def get_order_book(self, coin, limit = None):
        return super().get_order_book(coin, limit)

    def get_ohlcv(self, coin, since=None, limit=None, timeframe='1m'):
        return super().get_ohlcv(coin, since, limit, timeframe)

    async def get_ticker(self, coin, side=None):
        return await super().get_ticker(coin, side)

    # you need add a parameters checker
    async def create_order(self, coin, type, side, amount, price=None):
        if price is not None:
            result = await self.exchange.create_order(coin, type, side, amount, price)
        else:
            result = await self.exchange.create_order(coin, type, side, amount)

        print(result)
        if not result:
            print("Не удалось выполнить ордер.")
            return None

        order = self.get_order_history(1)
        print(order)
        order_stm = self.parse_order_to_clickhouse_format(order)
        if order_stm:
            self.monitoring.insert_single_order_to_db(order_stm)
        else:
            return None

        return result

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

    def create_market_buy_order(self, symbol, order_size):
        order = self.exchange.create_market_buy_order_with_cost(symbol, order_size)
        if order is not None:
            order_stm = self.parse_order_to_clickhouse_format(self.get_order_history(1))
            print(order_stm)
            self.monitoring.insert_single_order_to_db(order_stm[0])
            return order
        else:
            Exception

    def create_market_sell_order(self, symbol, order_size):
        order = self.exchange.create_market_sell_order_with_cost(symbol, order_size)
        if order is not None:
            order_stm = self.parse_order_to_clickhouse_format(self.get_order_history(1))
            print(order_stm)
            self.monitoring.insert_single_order_to_db(order_stm[0])
            return order
        else:
            Exception

    # def create_market_buy_order_with_cost(self, coin, cost):
    #     order = self.exchange.create_market_buy_order_with_cost(coin, cost)
    #     if order is not None:
    #         order_stm = self.get_order_history(1)
    #         self.monitoring.insert_single_order_to_db(order_stm)
    #         return order
    #     else:
    #         Exception
    #
    # def create_market_sell_order_with_cost(self, coin, cost):
    #     order = self.exchange.create_market_sell_order_with_cost(coin, cost)
    #     if order is not None:
    #         order_stm = self.get_order_history(1)
    #         self.monitoring.insert_single_order_to_db(order_stm)
    #         return order
    #     else:
    #         Exception

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

    def format_time_to_datetime(self, timestamp_str):
        return datetime.fromtimestamp(int(timestamp_str) / 1000) if timestamp_str else None

    def parse_order_to_clickhouse_format(self, response):
        if response.get('retCode') != 0:
            print("Invalid response")
            return []

        orders_list = response.get('result', {}).get('list', [])
        data_for_insertion = []

        for order in orders_list:
            order_data = {
                'orderId': order.get('orderId'),
                'exchange': 'bybit',
                'symbol': order.get('symbol'),
                'price': float(order.get('price', 0)),
                'qty': float(order.get('qty', 0)),
                'executedQty': float(order.get('executedQty', order.get('qty', 0))),
                'totalCost': float(order.get('cumExecValue', 0)),
                'side': order.get('side'),
                'orderType': order.get('orderType'),
                'orderStatus': order.get('orderStatus'),
                'createdTime': order.get('createdTime'),
                'updatedTime': order.get('updatedTime'),
                'commission': float(order.get('cumExecFee', 0))
            }
            data_for_insertion.append(order_data)

        return data_for_insertion








