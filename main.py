import os
from database.database import Database
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

database = Database('localhost', 8123, login_click, password_click)

# example use database:
columns = {
    'order_id': 'String',
    'symbol': 'String',
    'side': 'String',
    'order_type': 'String',
    'price': 'Float32',
    'amount': 'Float32',
    'cost': 'Float32',
    'fee': 'Float32',
    'created_time': 'DateTime'
}

columns = ['orderId', 'exchange', 'symbol', 'price', 'qty', 'executedQty', 'totalCost', 'side', 'orderType',
                        'orderStatus', 'createdTime', 'updatedTime', 'commission']

database.create_table('orders', columns)
