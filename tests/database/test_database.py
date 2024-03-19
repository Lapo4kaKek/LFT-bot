import pytest
from unittest.mock import MagicMock, patch
from database.database import Database
from datetime import datetime
import os
from utils.converter import Converter
from dotenv import load_dotenv

login_click = os.getenv('CLICKHOUSE_LOGIN')
password_click = os.getenv('CLICKHOUSE_PASSWORD')
port = os.getenv('CLICKHOUSE_PORT')

@pytest.fixture
def mock_clickhouse_client():
    return MagicMock()


@pytest.fixture
def database(mock_clickhouse_client):
    with patch('clickhouse_connect.get_client', return_value=mock_clickhouse_client):
        return Database(host='localhost', port=port, username=login_click, password=password_click)


def test_create_table(database, mock_clickhouse_client):
    columns = {'orderId': 'String', 'price': 'Float64'}
    database.create_table('test_orders', columns)
    mock_clickhouse_client.command.assert_called_once_with('CREATE TABLE IF NOT EXISTS test_orders (orderId String, price Float64) ENGINE = MergeTree() ORDER BY tuple()')


def test_insert_data(database, mock_clickhouse_client):
    table_name = 'test_orders'
    data = [('1234', 50.0)]
    column_names = ['orderId', 'price']
    database.insert_data(table_name, data, column_names)
    mock_clickhouse_client.insert.assert_called_once_with(table_name, data, column_names=column_names)


def test_format_time_to_datetime(database):
    timestamp = "1609459200000"  # Эквивалентно 01.01.2021 03:00:00 UTC+3
    expected_datetime = datetime(2021, 1, 1, 3, 0)
    assert database.format_time_to_datetime(timestamp) == expected_datetime

# def test_format_datetime_to_timestamp(database):
#     datetime_str = '2021-03-30 17:00:00'
#     expected_timestamp = '1617152400'
#     # assert database.format_datetime_to_timestamp(datetime_str) == expected_timestamp
#     assert Converter.format_datetime_to_timestamp(datetime_str) == expected_timestamp

def test_delete_all_data(database, mock_clickhouse_client):
    table_name = 'test_orders'
    database.delete_all_data(table_name)
    mock_clickhouse_client.command.assert_called_once_with(f'TRUNCATE TABLE {table_name}')


