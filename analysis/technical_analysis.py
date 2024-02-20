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

    def get_ohlcv(self, timeframe, since=None, limit=None):
        """
         Получает исторические данные OHLCV для указанной торговой пары и временного интервала.

        :param timeframe: Временной интервал данных (например, '1d' для одного дня).
        :param since: Начальная метка времени для загрузки данных (в миллисекундах). Если None, загрузка начинается с самой ранней доступной даты (зависит от биржи).
        :param limit: Максимальное количество возвращаемых записей. Если None, используется значение по умолчанию биржи.
        :return: DataFrame, содержащий колонки 'timestamp', 'open', 'high', 'low', 'close', 'volume', где 'timestamp' преобразован в формат datetime.
        """
        ohlcv = self.exchange.get_ohlcv(self.symbol, timeframe, since, limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
