import asyncio

import pandas as pd


class TechnicalAnalysis:
    """
    Класс TechnicalAnalysis предоставляет инструменты для загрузки и анализа исторических данных о ценах на криптовалютные активы.
    Использует библиотеку ccxt для взаимодействия с различными криптовалютными биржами.
    """

    def __init__(self, exchange, symbol):
        """
        Инициализация экземпляра класса TechnicalAnalysis.

        :param exchange: Экземпляр биржи, с которой будет производиться взаимодействие.
        :param symbol: Символ торговой пары, для которой будут запрашиваться данные.
        """
        self.exchange = exchange
        self.symbol = symbol
        self.df = None

    async def get_ohlcv(self, timeframe='1d', since=None, limit=None):
        """
         Получает исторические данные OHLCV для указанной торговой пары и временного интервала.

        :param timeframe: Временной интервал данных (например, '1d' для одного дня).
        :param since: Начальная метка времени для загрузки данных (в миллисекундах). Если None, загрузка начинается с самой ранней доступной даты (зависит от биржи).
        :param limit: Максимальное количество возвращаемых записей. Если None, используется значение по умолчанию биржи.
        :return: DataFrame, содержащий колонки 'timestamp', 'open', 'high', 'low', 'close', 'volume', где 'timestamp' преобразован в формат datetime.
        """
        ohlcv = await self.exchange.get_ohlcv(self.symbol, since, limit, timeframe)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        self.df = df
        return df

    def get_rsi(self, period=14):
        """
        Рассчитывает индекс относительной силы (RSI) для закрытия цен.

        :param period: Период для расчета RSI.
        :return: Series с значениями RSI.
        """
        delta = self.df['close'].diff()
        avg_gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        avg_loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def get_macd(self, fast_period=12, slow_period=26, signal_period=9):
        """
        Рассчитывает скользящую среднюю сходимость/расхождение (MACD).

        :param fast_period: Период быстрой EMA.
        :param slow_period: Период медленной EMA.
        :param signal_period: Период сигнальной линии.
        :return: Tuple из двух Series: (MACD, сигнальная линия).
        """

        exp1 = self.df['close'].ewm(span=fast_period, adjust=False).mean()
        exp2 = self.df['close'].ewm(span=slow_period, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=signal_period, adjust=False).mean()
        return macd, signal

    def get_aroon(self, period=25):
        """
        Рассчитывает индикаторы Aroon Up и Aroon Down.

        :param period: Период для расчета индикаторов Aroon.
        :return: Два объекта Series с индикаторами Aroon Up и Aroon Down.
        """
        high = self.df['high'].rolling(window=period).apply(lambda x: x.argmax(), raw=True) / (period - 1) * 100
        low = self.df['low'].rolling(window=period).apply(lambda x: x.argmin(), raw=True) / (period - 1) * 100
        return high, low

    def get_obv(self):
        """
        Рассчитывает объемный балансовый индикатор (On-Balance Volume, OBV).

        :return: Series с расчетными значениями OBV.
        """
        obv = (self.df['volume'] * (~self.df['close'].diff().le(0) * 2 - 1)).cumsum()
        return obv

    def get_stochastic_oscillator(self, k_period=14, d_period=3):
        """
        Рассчитывает стохастический осциллятор, включая %K и %D линии.

        :param k_period: Период для расчета %K.
        :param d_period: Период для расчета %D, скользящего среднего от %K.
        :return: Два объекта Series с %K и %D линиями стохастического осциллятора.
        """
        low = self.df['low'].rolling(window=k_period).min()
        high = self.df['high'].rolling(window=k_period).max()
        k_line = 100 * ((self.df['close'] - low) / (high - low))
        d_line = k_line.rolling(window=d_period).mean()
        return k_line, d_line

    def get_sma(self, period=30):
        """
        Рассчитывает простую скользящую среднюю (SMA).

        :param period: Период для расчета SMA.
        :return: Series с расчетными значениями SMA.
        """
        sma = self.df['close'].rolling(window=period).mean()
        return sma

    def get_ema(self, period=30):
        """
        Рассчитывает экспоненциальную скользящую среднюю (EMA).

        :param period: Период для расчета EMA.
        :return: Series с расчетными значениями EMA.
        """
        ema = self.df['close'].ewm(span=period, adjust=False).mean()
        return ema

    def get_bollinger_bands(self, period=20, std_dev=2):
        """
        Рассчитывает полосы Боллинджера.

        :param period: Период для расчета SMA в основе полос Боллинджера.
        :param std_dev: Количество стандартных отклонений для верхней и нижней полос.
        :return: Три объекта Series с верхней, средней (SMA) и нижней полосами.
        """
        sma = self.df['close'].rolling(window=period).mean()
        rstd = self.df['close'].rolling(window=period).std()
        upper_band = sma + std_dev * rstd
        lower_band = sma - std_dev * rstd
        return upper_band, sma, lower_band

    def get_momentum(self, period=14):
        """
        Рассчитывает моментум индикатор.

        :param period: Период для расчета моментума.
        :return: Series с расчетными значениями моментума.
        """
        momentum = self.df['close'].diff(period)
        return momentum
