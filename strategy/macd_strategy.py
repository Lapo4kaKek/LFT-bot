import asyncio
import os

from analysis.technical_analysis import TechnicalAnalysis
from exchange.binance_exchange import BinanceExchange
from exchange.bybit_exchange import BybitExchange
from strategy.base_strategy import BaseStrategy


class MACDStrategy(BaseStrategy):
    def __init__(self, exchange, balance, token, settings):
        """
        Конструктор.
        :param exchange: Биржа, на которой будет осуществляться торговля.
        :param balance: Выделенный на стратегию баланс.
        :param token: Токен, который будет торговаться.
        :param settings: Настройки стратегии, включающие в себя следующие пункты:
            - limit: Целое число, количество фреймов в запрашиваемом графике.
            - filter_days: Целое число, количество дней, в которые должен сохраняться тренд индикатора MACD для определения устойчивого тренда.
        """
        self.exchange = exchange
        self.balance = balance
        self.token = token
        self.settings = settings
        self.is_active = True
        # Экземпляр для получения технических индикаторов заданного токена.
        self.technical_indicators = TechnicalAnalysis(exchange, token + 'USDT')
        # Флаг, отвечающий за наличие открытой позиции на рынке.
        self.open_positions = False

    async def calculate_moving_averages(self):
        await self.technical_indicators.get_ohlcv(limit=self.settings['limit'])
        macd, signal = self.technical_indicators.get_macd()
        cross_upward = cross_downward = False
        cross_pos = -1
        for i in range(len(macd) - 1, 0, -1):
            cross_pos = i
            if signal[i] < macd[i] and macd[i - 1] <= signal[i - 1]:
                cross_upward = True
                break
            elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:
                cross_downward = True
                break
        if cross_downward:
            if cross_pos + self.settings['filter_days'] < self.settings['limit']:
                return -2
            return -1
        if cross_upward:
            if cross_pos + self.settings['filter_days'] < self.settings['limit']:
                return 2
            else:
                return 1
        return 0

    async def get_signal(self):
        result = await self.calculate_moving_averages()
        if self.open_positions and result < 0:
            return -1

        if not self.open_positions and result == 2:
            return 1

        return 0

    async def trading(self):
        """
        Осуществление асинхронной торговли в соответствии с заданными настройками.
        """
        while True:
            print(self.settings['strategy_name'] + ": ", end='')
            signal = await self.get_signal()
            if signal == 1:
                print('Buy')
            elif signal == -1:
                print('Sell')
            else:
                print('Hold')
            await asyncio.sleep(10)  # Пауза в 10 секунд

    def stop_strategy(self):
        """
        Остановка стратегии.
        """
        self.is_active = False


async def example():
    api_key_bybit = os.getenv('BYBIT_API_KEY')
    api_secret_bybit = os.getenv('BYBIT_API_SECRET')
    # Создание экземпляров стратегий
    bybit = BybitExchange(api_key_bybit, api_secret_bybit)
    strategy1 = MACDStrategy(exchange=bybit, balance=1000, token="BTC",
                             settings={'strategy_name': 'Strategy 1', 'filter_days': 3, 'limit': 100})

    # Запуск торговли для всех стратегий
    await asyncio.gather(
        strategy1.trading(),
    )


asyncio.run(example())
