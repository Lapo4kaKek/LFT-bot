import asyncio
from strategy.base_strategy import BaseStrategy


class DemoStrategy(BaseStrategy):
    def __init__(self, balance, token, settings):
        """
        Конструктор.
        :param balance: Начальный баланс стратегии.
        :param token: Токен, который будет торговаться.
        :param settings: Настройки стратегии.
        """
        self.balance = balance
        self.token = token
        self.settings = settings
        self.is_active = True  # флаг для управления выполнением стратегии

    def get_signals(self):
        """
        Получение и обработка сигналов.
        :return: Dict, содержащий списки ордеров на покупку ('buy') и продажу ('sell')
        """
        return {"buy": [], "sell": []}

    # Асинхронный метод, который будет вызываться в цикле
    async def trading(self):
        """
        Осуществление асинхронной торговли в соответствии с заданными настройками.
        """
        while True:
            signals = self.get_signals()

            for buy_signal in signals['buy']:
                pass

            for sell_signal in signals['sell']:
                pass

            print(self.settings['strategy_name'])
            await asyncio.sleep(10)  # Пауза в 10 секунд

    def stop_strategy(self):
        """
        Остановка стратегии.
        """
        self.is_active = False


# Инициализация и запуск нескольких стратегий
async def example():
    # Создание экземпляров стратегий
    strategy1 = DemoStrategy(balance=1000, token="BTC",
                             settings={'strategy_name': 'Strategy 1'})
    strategy2 = DemoStrategy(balance=2000, token="ETH",
                             settings={'strategy_name': 'Strategy 2'})
    strategy3 = DemoStrategy(balance=1500, token="XRP",
                             settings={'strategy_name': 'Strategy 3'})

    # Запуск торговли для всех стратегий
    await asyncio.gather(
        strategy1.trading(),
        strategy2.trading(),
        strategy3.trading(),
    )


asyncio.run(example())
