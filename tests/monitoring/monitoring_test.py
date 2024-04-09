import unittest
from unittest.mock import MagicMock, patch
from monitoring.monitoring import Monitoring

class TestMonitoring(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.monitoring = Monitoring(database=self.mock_db)
        self.sample_order = {
            'orderId': '12345',
            'exchange': 'test_exchange',
            'symbol': 'TEST',
            'price': '100.0',
            'qty': '10',
            'executedQty': '10',
            'totalCost': '1000.0',
            'side': 'buy',
            'orderType': 'market',
            'orderStatus': 'executed',
            'createdTime': '1609459200',  # Unix timestamp for 2021-01-01 00:00:00
            'updatedTime': '1609459200',
            'commission': '0.1',
            'stopPrice': '90.0'
        }
        self.sample_strategy_info = {
            'strategyId': 'strategy_123',
            'name': 'Test Strategy',
            'type': 'test_type',
            'exchange': 'test_exchange',
            'symbol': 'TEST',
            'balance': '10000',
            'assetsNumber': '100',
            'openPositions': True,
            'status': True,
            'createdTime': '1609459200',
            'settings': {}
        }

    def test_insert_orders_history_to_db(self):
        order_history = {
            'result': {
                'list': [
                    {
                        'orderId': 'test1',
                        'symbol': 'BTCUSD',
                        'price': '50000',
                        'qty': '1',
                        'side': 'buy',
                        'orderType': 'limit',
                        'orderStatus': 'filled',
                        'createdTime': '1609459200',  # Это UNIX timestamp для 2021-01-01 00:00:00
                        'updatedTime': '1609459200'
                    }
                ]
            }
        }

        # Имитация вызова методов базы данных
        self.mock_db.format_time_to_datetime.return_value = '2021-01-01 00:00:00'
        self.mock_db.insert_data.return_value = None

        # Выполнение тестируемого метода
        self.monitoring.insert_orders_history_to_db(order_history)

        # Проверка: был ли метод insert_data вызван с правильными аргументами
        self.mock_db.insert_data.assert_called_once_with(
            'orders',
            [
                (
                    'test1', 'BTCUSD', 50000.0, 1.0, 'buy', 'limit', 'filled',
                    '2021-01-01 00:00:00', '2021-01-01 00:00:00'
                )
            ],
            ['orderId', 'symbol', 'price', 'qty', 'side', 'order_type', 'order_status', 'created_time', 'updated_time']
        )

    def test_insert_single_order_to_db(self):
        self.monitoring.insert_single_order_to_db(self.sample_order)
        self.mock_db.insert_data.assert_called_once()

    def test_link_order_with_strategy(self):
        self.monitoring.link_order_with_strategy('12345', 'strategy_123')
        self.mock_db.insert_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()
