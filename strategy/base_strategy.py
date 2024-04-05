import time
from abc import ABC, abstractmethod

from analysis.technical_analysis import TechnicalAnalysis

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


class BaseStrategy(ABC):
    """
    Интерфейс для реализации стратегий.
    """

    def __init__(self, exchange, symbol, strategy_id, monitoring, settings, balance, type):
        self.exchange = exchange
        self.symbol = symbol
        self.settings = settings
        # Экземпляр для получения технических индикаторов заданного токена.
        self.technical_indicators = TechnicalAnalysis(exchange, symbol)
        # strategy_id для связи в clickhouse.
        self.strategy_id = strategy_id
        # Класс мониторинга для добавления в clickhouse.
        self.monitoring = monitoring
        self.type = type
        self.register_strategy(balance)
        self.info = None

    def register_strategy(self, balance):
        """
        Регистрирует стратегию в ClickHouse
        """
        current_time = int(time.time() * 1000)

        strategy_info = {
            'strategyId': self.strategy_id,
            'type': self.type,
            'name': self.settings.get('strategy_name', 'Unnamed Strategy'),
            'exchange': self.exchange.exchange_name,
            'symbol': self.symbol,
            'balance': balance,
            'assetsNumber': 0,
            'openPositions': False,
            'status': False,
            'createdTime': current_time
        }

        self.monitoring.insert_strategy_info(strategy_info)

    async def create_strategy(self):
        await self.update_info()

    async def update_info(self):
        self.info = await self.monitoring.get_strategy_info(self.strategy_id)


    @abstractmethod
    def get_signal(self):
        """
        Генерирует финальный торговый сигнал, который указывает на
        необходимость открыть или закрыть позицию.

        :return: Сигнал к действию: -1 для продажи (закрытия позиции),
        1 для покупки (открытия позиции), 0 для отсутствия действий.
        """
        pass

    @abstractmethod
    async def trading(self):
        """
        Запуск асинхронной торговли.
        """
        pass

    def stop_strategy(self):
        """
        Остановка стратегии.
        """
        pass
