import asyncio
import threading
import time
import uuid
import os
from dotenv import load_dotenv

from exchange.bybit_exchange import BybitExchange
from strategy.macd_strategy import MACDStrategy

strategies_types = {
    'MACD': {
        'type': 'macd',
        'exchange': 'bybit',
        'symbol': 'BTCUSDT',
        'strategy_name': 'Strategy 1',
        'balance': 1000,
        'settings': {
            'filter_days': 3,
            'limit': 100,
            'loss_coef': 0.8
        }
    },
    'example1': '',
    'example2': ''
}


def register_strategy(monitoring, name, strategy_type, exchange, symbol, balance, settings):
    """
    Регистрирует стратегию в ClickHouse
    """
    current_time = int(time.time() * 1000)
    strategy_id = str(uuid.uuid4())
    strategy_info = {
        'strategyId': strategy_id,
        'type': strategy_type,
        'name': name,
        'exchange': exchange,
        'symbol': symbol,
        'balance': balance,
        'assetsNumber': 0,
        'openPositions': False,
        'status': False,
        'createdTime': current_time,
        'settings': settings
    }

    monitoring.insert_strategy_info(strategy_info)
    return strategy_id


def start_strategy(strategy_id, monitoring):
    load_dotenv()

    info = asyncio.run(monitoring.get_strategy_info(strategy_id))
    exchange = None
    if info['exchange'] == 'bybit':
        api_key_bybit = os.getenv('BYBIT_API_TESTNET')
        api_secret_bybit = os.getenv('BYBIT_API_SECRET_TESTNET')
        exchange = BybitExchange(api_key_bybit, api_secret_bybit, monitoring)
        exchange.exchange.set_sandbox_mode(True)

    strategy = None
    if info['type'] == 'macd':
        strategy = MACDStrategy(exchange, info['symbol'], strategy_id, monitoring)

    asyncio.run(monitoring.update_strategy_info(strategy_id=strategy_id, data={
        'status': True
    }))

    thread = threading.Thread(target=strategy.trading)
    thread.start()
    print("START: ", info)


def stop_strategy(strategy_id, monitoring):
    info = asyncio.run(monitoring.get_strategy_info(strategy_id))
    print("STOP: ", info)