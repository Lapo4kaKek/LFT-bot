import time
import uuid

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


