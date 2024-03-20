import asyncio
import os
from dotenv import load_dotenv

from analysis.technical_analysis import TechnicalAnalysis
from decimal import *
from exchange.binance_exchange import BinanceExchange
from exchange.bybit_exchange import BybitExchange
from strategy.base_strategy import BaseStrategy


class MACDStrategy(BaseStrategy):
    def __init__(self, exchange, balance, symbol, settings, strategy_id):
        """
        Конструктор.
        :param exchange: Биржа, на которой будет осуществляться торговля.
        :param balance: Выделенный на стратегию баланс.
        :param symbol: Символ торговой пары.
        :param settings: Настройки стратегии, включающие в себя следующие пункты:
            - limit: Целое число, количество фреймов в запрашиваемом графике.
            - filter_days: Целое число, количество дней, в которые должен сохраняться тренд индикатора MACD для определения устойчивого тренда.
        :param strategy_id: Уникальный идентификатор стратегии.
        """
        self.exchange = exchange
        self.balance = balance
        self.symbol = symbol
        self.settings = settings
        self.is_active = True
        # Экземпляр для получения технических индикаторов заданного токена.
        self.technical_indicators = TechnicalAnalysis(exchange, symbol)
        # Флаг, отвечающий за наличие открытой позиции на рынке.
        self.open_positions = False
        # strategy_id для связи в clickhouse
        self.strategy_id = strategy_id

    async def calculate_moving_averages(self):
        """
        Асинхронно рассчитывает индикаторы MACD и сигнальную линию для определения
        моментов пересечения, что может указывать на потенциальные точки входа или выхода из рынка.

        Использует настройки стратегии, такие как 'limit' и 'filter_days'.

        :return: Число, указывающее на тип пересечения и его значимость (чем выше абсолютное значение, тем выше значимость):
        -2 или -1 для пересечения вниз, 2 или 1 для пересечения вверх, 0 если пересечений не обнаружено.
        """
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
        """
        Генерирует финальный торговый сигнал, который указывает на
        необходимость открыть или закрыть позицию.

        :return: Сигнал к действию: -1 для продажи (закрытия позиции),
        1 для покупки (открытия позиции), 0 для отсутствия действий.
        """
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
        """
        params={
        'stopLoss': {
            'type': 'market',
            'price': price * Decimal(self.settings['loss_coef'])
        }}
        """
        while True:
            print(self.settings['strategy_name'] + ": ", end='')
            signal = await self.get_signal()
            if signal == 0:
                order = self.exchange.create_market_buy_order_native(symbol=self.symbol, order_size=self.balance,
                                                                     testnet=True, strategy_id=self.strategy_id)
                self.open_positions = True
                # order = await self.exchange.create_order(coin=self.symbol, type='market', side='sell',
                #                                          amount=self.balance / price, price=None, params={
                #         'stopLossPrice': price * Decimal(self.settings['loss_coef']),
                #         }
                # )
                # print(order)
                print('Buy')
            elif signal == -1:
                order = self.exchange.create_market_sell_order_native(symbol=self.symbol, order_size=0.02,
                                                                      testnet=True, strategy_id=self.strategy_id)
                self.open_positions = False
                print('Sell')
            else:
                print('Hold')
            await asyncio.sleep(10)  # Пауза в 10 секунд

    def stop_strategy(self):
        """
        Остановка стратегии.
        """
        self.is_active = False
