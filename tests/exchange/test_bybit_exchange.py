import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock
from exchange.bybit_exchange import BybitExchange

class TestBybitExchange(unittest.TestCase):
    def setUp(self):
        self.api_key = 'fake_api_key'
        self.api_secret = 'fake_api_secret'
        self.monitoring = MagicMock()
        self.bybit_exchange = BybitExchange(self.api_key, self.api_secret, self.monitoring)
        self.bybit_exchange.exchange.create_order = AsyncMock()
        self.bybit_exchange.exchange.fetch_closed_orders = AsyncMock()
        self.bybit_exchange.exchange.fetch_open_orders = AsyncMock()
        self.bybit_exchange.session.get_executions = MagicMock()

    def test_create_market_buy_order(self):
        symbol = 'BTC/USD'
        order_size = 1

        self.bybit_exchange.exchange.create_order.return_value = {'status': 'order_placed'}
        self.bybit_exchange.exchange.fetch_closed_orders.return_value = [{'timestamp': 123456789, 'id': 'test_order_id'}]
        self.bybit_exchange.parse_order_to_clickhouse_format_ccxt = MagicMock()

        result = asyncio.run(self.bybit_exchange.create_market_buy_order(symbol, order_size))

        self.bybit_exchange.exchange.create_order.assert_awaited_once_with(symbol, 'market', 'buy', order_size, params={})
        self.bybit_exchange.exchange.fetch_closed_orders.assert_awaited_once_with(symbol)
        self.bybit_exchange.parse_order_to_clickhouse_format_ccxt.assert_called_once()

    def test_create_market_sell_order(self):
        symbol = 'BTC/USD'
        order_size = 1
        order_id = '1'

        self.bybit_exchange.create_order = MagicMock(return_value={'result': {'orderId': order_id}})

        self.bybit_exchange.session.get_executions.return_value = {'result': {'orderId': order_id}}

        self.bybit_exchange.create_market_sell_order(symbol, order_size)

        self.bybit_exchange.session.get_executions.assert_called_once_with(category="spot", orderId=order_id, limit=1)


if __name__ == '__main__':
    unittest.main()
