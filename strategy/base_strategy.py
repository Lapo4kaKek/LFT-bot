from abc import ABC, abstractmethod

strategies_types = {
    'macd': '',
    'example1': '',
    'example2': ''
}


class BaseStrategy(ABC):
    """
    Интерфейс для реализации стратегий.
    """

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
