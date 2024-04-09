import asyncio
import os
import threading

import telebot

import telegram_bot
from database.database import Database
from dotenv import load_dotenv
import ccxt
from datetime import datetime
from exchange.bybit_exchange import BybitExchange
from monitoring.monitoring import Monitoring
from multiprocessing import Process

from strategy import strategy_manager
from telegram_bot.handlers import TelegramBotHandlers

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

orders_columns = {
    'orderId': 'String',
    'exchange': 'String',
    'symbol': 'String',
    'price': 'Decimal(38, 20)',
    'stopPrice': 'Decimal(38, 20)',
    'qty': 'Decimal(38, 20)',
    'executedQty': 'Decimal(38, 20)',
    'totalCost': 'Decimal(38, 20)',
    'side': 'String',
    'orderType': 'String',
    'orderStatus': 'String',
    'createdTime': 'DateTime',
    'updatedTime': 'DateTime',
    'commission': 'Decimal(38, 20)'
}
database.create_table('orders', orders_columns)

strategies_columns = {
    'strategyId': 'String',
    'name': 'String',
    'type': 'String',
    'exchange': 'String',
    'symbol': 'String',
    'balance': 'Decimal(38, 20)',
    'assetsNumber': 'Decimal(38, 20)',
    'openPositions': 'Boolean',
    'status': 'Boolean',
    'createdTime': 'DateTime',
    'settings': 'Map(String, Double)'
}
database.create_table('strategies', strategies_columns)

order_strategy_link_columns = {
    'orderId': 'String',
    'strategyId': 'String'
}
database.create_table('order_strategy_link', order_strategy_link_columns)

if __name__ == '__main__':
    monitoring = Monitoring(database)
    strategies = monitoring.get_launched_strategies()
    for strategy in strategies:
        strategy_manager.start_strategy(strategy['strategyId'], first_launch=True)

    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    bot = TelegramBotHandlers(monitoring, database, telegram_bot_token)

    # thread1 = threading.Thread(target=func)
    thread2 = threading.Thread(target=bot.start_bot)

    # Запуск потоков
    #thread1.start()
    thread2.start()

    # Ожидание завершения обоих потоков
    # thread1.join()
    thread2.join()



