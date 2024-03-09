from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """
    Интерфейс для реализации стратегий.
    """

    @abstractmethod
    def get_signals(self):
        """
        Получение и обработка сигналов.
        :return: Dict, содержащий списки ордеров на покупку ('buy') и продажу ('sell')
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
