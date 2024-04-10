from unittest.mock import MagicMock, patch
from database.database import Database
from datetime import datetime
import os
from utils.converter import Converter
from dotenv import load_dotenv

login_click = os.getenv('CLICKHOUSE_LOGIN')
password_click = os.getenv('CLICKHOUSE_PASSWORD')
port = os.getenv('CLICKHOUSE_PORT')


import unittest
from unittest.mock import MagicMock, patch
from database.database import Database
from datetime import datetime

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.mock_clickhouse_client = MagicMock()
        self.database = Database(
            host='localhost',
            port=8123,
            username='admin',
            password='admin'
        )
        self.database.client = self.mock_clickhouse_client

    def test_create_table(self):
        table_name = 'test_orders'
        columns = {'orderId': 'String', 'price': 'Float64'}
        self.database.create_table(table_name, columns)
        create_table_query = 'CREATE TABLE IF NOT EXISTS test_orders (orderId String, price Float64) ENGINE = MergeTree() ORDER BY tuple()'
        self.mock_clickhouse_client.command.assert_called_once_with(create_table_query)

    def test_insert_data(self):
        table_name = 'test_orders'
        data = [('1234', 50.0)]
        column_names = ['orderId', 'price']
        self.database.insert_data(table_name, data, column_names=column_names)
        self.mock_clickhouse_client.insert.assert_called_once_with(table_name, data, column_names=column_names)

    def test_format_time_to_datetime(self):
        timestamp_str = "1609459200000"  # Эквивалентно 01.01.2021 00:00:00 UTC
        expected_datetime = datetime.utcfromtimestamp(int(timestamp_str) / 1000)
        self.assertEqual(self.database.format_time_to_datetime(timestamp_str), expected_datetime)

    def test_delete_all_data(self):
        table_name = 'test_orders'
        self.database.delete_all_data(table_name)
        delete_query = f'TRUNCATE TABLE {table_name}'
        self.mock_clickhouse_client.command.assert_called_once_with(delete_query)

    def test_execute_query(self):
        query = "SELECT * FROM test_table"
        params = {"param1": "value1"}
        self.database.execute_query(query, params)
        self.mock_clickhouse_client.query.assert_called_once_with(query, params)

    def test_create_table_failure(self):
        table_name = 'test_orders'
        columns = {'orderId': 'String', 'price': 'Float64'}
        self.mock_clickhouse_client.command.side_effect = Exception('Create table failed')

        with self.assertRaises(Exception) as context:
            self.database.create_table(table_name, columns)

        self.assertEqual(str(context.exception), 'Create table failed')

    def test_insert_data_failure(self):
        table_name = 'test_orders'
        data = [('1234', 50.0)]
        column_names = ['orderId', 'price']
        self.mock_clickhouse_client.insert.side_effect = Exception('Insert failed')

        with self.assertRaises(Exception) as context:
            self.database.insert_data(table_name, data, column_names=column_names)

        self.assertEqual(str(context.exception), 'Insert failed')

    def test_execute_query_without_columns(self):
        query = "SELECT * FROM test_table"
        self.mock_clickhouse_client.query.return_value.result_rows = [('row1',), ('row2',)]

        result = self.database.execute_query(query, columns=False)

        self.assertEqual(result, [('row1',), ('row2',)])
        self.mock_clickhouse_client.query.assert_called_once_with(query, {})

    def test_execute_query_without_params(self):
        query = "SELECT * FROM test_table"
        self.mock_clickhouse_client.query.return_value.result_rows = [('row1',), ('row2',)]

        result = self.database.execute_query(query)

        self.assertEqual(result, [('row1',), ('row2',)])
        self.mock_clickhouse_client.query.assert_called_once_with(query, {})


if __name__ == '__main__':
    unittest.main()


