import unittest
from unittest.mock import MagicMock, patch
from monitoring.monitoring import Monitoring
import unittest
from unittest.mock import MagicMock, patch
from monitoring.monitoring import Monitoring
import re

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
    def test_delete_strategy(self):
        strategy_id = 'strategy_123'
        self.monitoring.delete_strategy(strategy_id)
        expected_query = "DELETE FROM strategies WHERE strategyId = 'strategy_123';"
        self.mock_db.execute_query.assert_called_once_with(expected_query.strip())

    def test_get_strategy_info(self):
        strategy_id = 'strategy_123'
        result = self.monitoring.get_strategy_info(strategy_id)
        expected_query = "SELECT * FROM strategies WHERE strategyId == 'strategy_123'"
        self.mock_db.execute_query.assert_called_once_with(expected_query.strip(), columns=True)

    def test_update_strategy_info(self):
        strategy_id = 'strategy_123'
        update_data = {'status': False}
        self.monitoring.update_strategy_info(strategy_id, update_data)
        condition = "status = False"
        expected_query = f"ALTER TABLE strategies UPDATE {condition} WHERE strategyId = 'strategy_123'"
        self.mock_db.execute_query.assert_called_once_with(expected_query)

    def test_calculate_and_insert_daily_pnl(self):
        orders_data = [{
            'created_time': '2021-01-01 00:00:00',
            'price': 50000.0,
            'qty': 1.0,
            'side': 'sell',
        }]

        starting_capital = 100000
        self.monitoring.calculate_and_insert_daily_pnl(orders_data, starting_capital)
        expected_data = [
            ('2021-01-01 00:00:00', 50000.0, 50.0)
        ]
        self.mock_db.insert_data.assert_called_once_with(
            'daily_pnl', expected_data, ['date', 'daily_pnl', 'pnl_percentage']
        )


    def test_delete_strategy(self):
        strategy_id = 'strategy_123'
        expected_query = "DELETE FROM strategies WHERE strategyId = 'strategy_123';"
        self.monitoring.delete_strategy(strategy_id)
        assert_query_called_with(self.mock_db.execute_query, expected_query)

    def test_get_strategy_info(self):
        strategy_id = 'strategy_123'
        expected_query = "SELECT * FROM strategies WHERE strategyId == 'strategy_123'"
        result = self.monitoring.get_strategy_info(strategy_id)
        assert_query_called_with(self.mock_db.execute_query, expected_query, columns=True)


def assert_query_called_with(mock_call, expected_query, **kwargs):
    # Эта функция удаляет все пробелы из ожидаемого запроса
    # и из фактического вызова для прямого сравнения
    call_args, call_kwargs = mock_call.call_args
    actual_query = call_args[0]

    expected_query = re.sub(r'\s+', '', expected_query)
    actual_query = re.sub(r'\s+', '', actual_query)

    assert expected_query == actual_query, f"Ожидаемый запрос не соответствует фактическому.\nОжидаемый: {expected_query}\nФактический: {actual_query}"
    assert call_kwargs == kwargs, f"Ожидаемые kwargs не соответствуют фактическим.\nОжидаемый: {kwargs}\nФактический: {call_kwargs}"

if __name__ == '__main__':
    unittest.main()

