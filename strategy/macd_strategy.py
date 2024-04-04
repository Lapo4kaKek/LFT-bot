import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
from analysis.technical_analysis import TechnicalAnalysis
from decimal import *
from exchange.binance_exchange import BinanceExchange
from exchange.bybit_exchange import BybitExchange
from strategy.base_strategy import BaseStrategy
import time


class MACDStrategy(BaseStrategy):
    def __init__(self, exchange, symbol, strategy_id, monitoring, settings, balance):
        """
        Конструктор. :param exchange: Биржа, на которой будет осуществляться торговля. :param symbol: Символ торговой
        пары. :param strategy_id: Уникальный идентификатор стратегии. :param monitoring: инстанс мониторинга для
        добавления в clickhouse. :param settings: Настройки стратегии, включающие в себя следующие пункты: - limit:
        Целое число, количество фреймов в запрашиваемом графике. - filter_days: Целое число, количество дней,
        в которые должен сохраняться тренд индикатора MACD для определения устойчивого тренда.
        """
        super().__init__(exchange, symbol, strategy_id, monitoring, settings, balance, 'MACD')

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
        if self.info['openPositions'] and result < 0:
            return -1

        if not self.info['openPositions'] and result == 2:
            return 1

        return 0

    async def trading(self):
        """
        Осуществление асинхронной торговли в соответствии с заданными настройками.
        """
        while True:
            await self.update_info()
            print(self.settings['strategy_name'] + ": ", end='')
            signal = await self.get_signal()
            print("Signal: " + str(signal))
            if signal == 0:
                ticker = await self.exchange.get_ticker(self.symbol, 'buy')
                order = await self.exchange.create_market_buy_order(symbol=self.symbol,
                                                                    order_size=Decimal(self.info['balance']) / Decimal(ticker[0]))
                await self.monitoring.update_strategy_info(strategy_id=self.strategy_id, data={'assetsNumber': order['filled'], 'openPositions': True})
                order = await self.exchange.create_market_stop_loss_order(symbol=self.symbol, order_size=order['filled'], params={
                    'triggerPrice': Decimal(ticker[0]) * Decimal(self.settings['loss_coef']),
                    'triggerDirection': 'below'
                })

                print("STOP LOSS: ", order)
                print('Buy\n----------------------')
            elif signal == -1:
                order = self.exchange.create_market_sell_order_native(symbol=self.symbol, order_size=0.02,
                                                                      testnet=True, strategy_id=self.strategy_id)
                self.open_positions = False
                print('Sell\n----------------------')
            else:
                print('Hold')
            print(self.exchange.get_trade_history())
            print(self.exchange.get_order_history())

            await asyncio.sleep(10)  # Пауза в 10 секунд

    async def stop_strategy(self):
        """
        Остановка стратегии.
        """
        self.update_strategy_info()
        self.is_active = False
