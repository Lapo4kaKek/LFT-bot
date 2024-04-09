import asyncio

from .base_exchange import BaseExchange

import ccxt.async_support as ccxt
from pybit.unified_trading import HTTP
from utils.converter import Converter
from datetime import datetime
import hashlib
import hmac
import json
import requests
import urllib3
import time
import uuid
from urllib.parse import quote_plus


class BybitExchange(BaseExchange):
    def __init__(self, api_key, api_secret, monitoring):
        """
        Инициализирует экземпляр BinanceExchange с использованием предоставленных API key и API secret.
        :param api_key: API ключ пользователя для доступа к Bybit.
        :param api_secret: Секретный ключ пользователя для доступа к Bybit.
        """
        super().__init__(api_key, api_secret)
        self.exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret,
        })
        self.session = HTTP(
            testnet=True,
            api_key=self.api_key,
            api_secret=self.api_secret,
        )
        self.monitoring = monitoring
        # добавил это поле для добавления в стратегию параметры 'exchange'
        self.exchange_name = 'bybit'

    def get_order_book(self, coin, limit=None):
        return super().get_order_book(coin, limit)

    def get_ohlcv(self, coin, since=None, limit=None, timeframe='1m'):
        return super().get_ohlcv(coin, since, limit, timeframe)

    async def get_ticker(self, coin, side=None):
        return await super().get_ticker(coin, side)

    # you need add a parameters checker
    async def create_order(self, coin, type, side, amount, price=None, params={}):
        if price is not None:
            result = await self.exchange.create_order(coin, type, side, amount, price, params=params)
        else:
            result = await self.exchange.create_order(coin, type, side, amount, params=params)

        # print(result)
        # if not result:
        #     print("Не удалось выполнить ордер.")
        #     return None
        #
        # order = self.get_order_history(1)
        # print(order)
        # order_stm = self.parse_order_to_clickhouse_format(order)
        # if order_stm:
        #     self.database.insert_single_order_to_db(order_stm)
        # else:
        #     return None

        return result

    async def get_balance(self):
        return await super().get_balance()

    # futures
    def set_leverage(self, coin, level):
        """

        :param coin: Example: SOL/USDT = SOLUSDT
        :param level:
        :return:
        """
        return self.exchange.set_leverage(level, coin)

    async def create_market_buy_order(self, strategy_id, symbol, order_size, params={}):
        response_data = await self.create_order(symbol, 'market', 'buy', order_size, params=params)
        await asyncio.sleep(1)
        closed_orders = await self.exchange.fetch_closed_orders(symbol)
        sorted_by_timestamp = self.exchange.sort_by(closed_orders, 'timestamp', True)
        order = sorted_by_timestamp[0]
        if order is not None:
            order_stm = self.parse_order_to_clickhouse_format_ccxt(order)
            print("Order_stm: ", order_stm)
            self.monitoring.insert_single_order_to_db(order_stm)
            self.monitoring.link_order_with_strategy(order_stm['orderId'], strategy_id)
            return order
        else:
            Exception

    async def create_market_sell_order(self, strategy_id, symbol, order_size, params={}):
        response_data = await self.create_order(symbol, 'market', 'sell', order_size, params=params)
        await asyncio.sleep(1)
        closed_orders = await self.exchange.fetch_closed_orders(symbol)
        sorted_by_timestamp = self.exchange.sort_by(closed_orders, 'timestamp', True)
        order = sorted_by_timestamp[0]
        if order is not None:
            order_stm = self.parse_order_to_clickhouse_format_ccxt(order)
            print("Order_stm: ", order_stm)
            self.monitoring.insert_single_order_to_db(order_stm)
            self.monitoring.link_order_with_strategy(order_stm['orderId'], strategy_id)
            return order
        else:
            Exception

    async def create_market_stop_loss_order(self, strategy_id, symbol, order_size, params={}):
        response_data = await self.create_order(symbol, 'market', 'sell', order_size, params=params)
        await asyncio.sleep(1)
        open_orders = await self.exchange.fetch_open_orders(symbol)
        sorted_by_timestamp = self.exchange.sort_by(open_orders, 'timestamp', True)
        order = sorted_by_timestamp[0]
        if order is not None:
            order_stm = self.parse_order_to_clickhouse_format_ccxt(order)
            print("Order_stm: ", order_stm)
            self.monitoring.insert_single_order_to_db(order_stm)
            self.monitoring.link_order_with_strategy(order_stm['orderId'], strategy_id)
            return order
        else:
            Exception

    def parse_order_to_clickhouse_format_ccxt(self, order):
        # created_time = self.format_time_to_datetime(str(response.get('time')))
        # updated_time = self.format_time_to_datetime(str(order.get('execTime', response.get('time'))))
        order_data = {
            'orderId': order.get('id'),
            'exchange': 'bybit',
            'symbol': order.get('symbol'),
            'orderType': order.get('type'),
            'side': order.get('side'),
            'price': float(0 if order.get('price', 0) is None else order.get('price', 0)),
            'stopPrice': float(0 if order.get('stopPrice', 0) is None else order.get('stopPrice', 0)),
            'executedQty': float(order.get('filled', 0)),
            'qty': float(order.get('amount', 0)),
            'totalCost': float(order.get('cost', 0)),
            'orderStatus': order.get('status'),
            'createdTime': order.get('timestamp'),
            'updatedTime': order.get('lastTradeTimestamp'),
            'commission': float( order.get('fee', {}).get('cost', 0))
        }

        return order_data

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

    def format_time_to_datetime(self, timestamp_str):
        return datetime.fromtimestamp(int(timestamp_str) / 1000) if timestamp_str else None

    def parse_order_to_clickhouse_format(self, response):
        if response.get('retCode') != 0:
            print("Invalid response")
            return []

        orders_list = response.get('result', {}).get('list', [])
        data_for_insertion = []

        for order in orders_list:
            order_status = 'Filled' if order.get('leavesQty') == '0' else 'Partial'
            # created_time = self.format_time_to_datetime(str(response.get('time')))
            # updated_time = self.format_time_to_datetime(str(order.get('execTime', response.get('time'))))

            order_data = {
                'orderId': order.get('orderId'),
                'exchange': 'bybit',
                'symbol': order.get('symbol'),
                'price': float(order.get('execPrice', 0)),
                'qty': float(order.get('execQty', 0)),
                'executedQty': float(order.get('execQty', 0)),
                'totalCost': float(order.get('execValue', 0)),
                'side': order.get('side'),
                'orderType': order.get('orderType'),
                'orderStatus': order_status,
                'createdTime': response.get('time'),
                'updatedTime': response.get('time'),
                'commission': float(order.get('execFee', 0))
            }
            data_for_insertion.append(order_data)

        return data_for_insertion

    def create_market_buy_order_native(self, symbol, order_size, testnet=False, **kwargs):
        params = kwargs.get('params', {})
        strategy_id = kwargs.get('strategy_id', '0')
        if testnet == True:
            self.session = HTTP(
                testnet=True,
                api_key=self.api_key,
                api_secret=self.api_secret,
            )
        response_data = self.session.place_order(
            category="spot",
            symbol=symbol,
            side="Buy",
            orderType="Market",
            qty=order_size,
            params=params
        )
        time.sleep(1)
        order_id = response_data['result']['orderId']
        print("Order id:" + order_id)
        order = self.session.get_executions(
            category="spot",
            orderId=f'{order_id}',
            limit=1,
        )
        print("Order:")
        print(order)

        if order is not None:
            order_stm = self.parse_order_to_clickhouse_format(order)
            print(order_stm)
            self.monitoring.insert_single_order_to_db(order_stm[0])
            self.monitoring.link_order_with_strategy(f'{order_id}', strategy_id)
            return order
        else:
            Exception


    def get_executions(self, order_id, category="spot", limit = 1):
        order = self.session.get_executions(
            category=category,
            order_id=f'{order_id}',
            limit=limit
        )
        return order

    def create_market_sell_order_native(self, symbol, order_size, testnet=False, **kwargs):
        strategy_id = kwargs.get('strategy_id', '0')
        if testnet == True:
            self.session = HTTP(
                testnet=True,
                api_key=self.api_key,
                api_secret=self.api_secret,
            )
        response_data = self.session.place_order(
            category="spot",
            symbol=symbol,
            side="Sell",
            orderType="Market",
            qty=order_size,
        )
        time.sleep(1)
        order_id = response_data['result']['orderId']
        print("Order id:" + order_id)
        order = self.session.get_executions(
            category="spot",
            orderId=f'{order_id}',
            limit=1,
        )
        print("Order:")
        print(order)

        if order is not None:
            order_stm = self.parse_order_to_clickhouse_format(order)
            print(order_stm)
            self.monitoring.insert_single_order_to_db(order_stm[0])
            self.monitoring.link_order_with_strategy(f'{order_id}', strategy_id)
            return order
        else:
            Exception

    def get_balance_native(self, coin, testnet=False):
        if testnet == True:
            self.session = HTTP(
                testnet=True,
                api_key=self.api_key,
                api_secret=self.api_secret,
            )
        result = self.session.get_wallet_balance(
            accountType="UNIFIED",
            coin="SOL",
        )

        return result

    async def close(self):
        """
        Закрывает все ресурсы, связанные с экземпляром BybitExchange.
        """
        if hasattr(self.session, 'close'):
            await self.session.close()

        if hasattr(self.exchange, 'close'):
            await self.exchange.close()