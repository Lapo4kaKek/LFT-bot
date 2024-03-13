import os
from monitoring.monitoring import Monitoring
from dotenv import load_dotenv
import ccxt
from datetime import datetime

from exchange.bybit_exchange import BybitExchange
# import ccxt
# from exchange.binance_exchange import BinanceExchange
# from exchange.hyperliquid_exchange import HyperLiquidExchange
# from analysis.technical_analysis import TechnicalAnalysis

#
# from utils.converter import Converter
# from eth_utils import from_wei, to_hex
# from eth_account.account import Account

load_dotenv()

api_key_bybit = os.getenv('BYBIT_API_KEY')
api_secret_bybit = os.getenv('BYBIT_API_SECRET')

login_click = os.getenv('CLICKHOUSE_LOGIN')
password_click = os.getenv('CLICKHOUSE_PASSWORD')

monitoring = Monitoring('localhost', 8123, login_click, password_click)

# Инициализация
# monitoring = Monitoring(host='localhost', port=8123, username='default', password='')

# Создание таблицы
columns = {
    'order_id': 'String',
    'symbol': 'String',
    'price': 'Float64',
    'qty': 'Float64',
    'side': 'String',
    'order_type': 'String',
    'order_status': 'String',
    'created_time': 'DateTime',
    'updated_time': 'DateTime'
}
#monitoring.create_table('orders', columns)
def format_time_to_datetime(timestamp_str):
    return datetime.fromtimestamp(int(timestamp_str) / 1000)
def insert_order_history_to_db(bybit_exchange, monitoring_instance):
    order_history = bybit_exchange.get_order_history(10)
    data = []
    # print("Check:")
    # print(order_history['result']['list'])
    # Extract relevant data from each order
    for order in order_history['result']['list']:
        data.append((
            order['orderId'],
            order['symbol'],
            float(order['price']),
            float(order['qty']),
            order['side'],
            order['orderType'],
            order['orderStatus'],
            format_time_to_datetime(order['createdTime']),
            format_time_to_datetime(order['updatedTime'])
        ))


    # Define the column names in the same order as the data
    column_names = ['order_id', 'symbol', 'price', 'qty', 'side', 'order_type', 'order_status', 'created_time', 'updated_time']

    # Insert data into the database
    table_name = 'orders'  # Change this to your actual table name
    monitoring_instance.insert_data(table_name, data, column_names)

bybit = BybitExchange(api_key_bybit, api_secret_bybit)

# insert_order_history_to_db(bybit, monitoring)
#monitoring.fetch_and_print_table_data("orders")

monitoring.calculate_and_insert_daily_pnl(bybit.get_order_history(20), 100)