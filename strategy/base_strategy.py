import time
from abc import ABC, abstractmethod
from analysis.technical_analysis import TechnicalAnalysis


class BaseStrategy(ABC):
    """
    Интерфейс для реализации стратегий.
    """

    def __init__(self, exchange, symbol, strategy_id, monitoring):
        self.exchange = exchange
        self.symbol = symbol
        # Экземпляр для получения технических индикаторов заданного токена.
        self.technical_indicators = TechnicalAnalysis(exchange, symbol)
        # strategy_id для связи в clickhouse.
        self.strategy_id = strategy_id
        # Класс мониторинга для добавления в clickhouse.
        self.monitoring = monitoring
        self.info = None

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
