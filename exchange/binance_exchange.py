import ccxt
from .base_exchange import BaseExchange


class BinanceExchange(BaseExchange):
    """
    Предоставляет специализированные методы для работы с криптовалютной биржей Binance.
    """
    def __init__(self, api_key, api_secret):
        """
        Инициализирует экземпляр BinanceExchange с использованием предоставленных API key и API secret.
        :param api_key: API ключ пользователя для доступа к Binance.
        :param api_secret: Секретный ключ пользователя для доступа к Binance.
        """
        super().__init__(api_key, api_secret)
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
        })

    def get_order_book(self, symbol):
        """

        :param symbol: Символ торговой пары, для которой требуется получить стакан ордеров.
        :return: dict: Стакан ордеров для указанной торговой пары.
        """
        return self.exchange.fetch_order_book(symbol)

    def get_ticker(self, symbol, side=None):
        """
        Возвращает информацию о последних ценах и объемах для заданной торговой пары.
        Может возвращать данные конкретно для покупки или продажи, если указан параметр side.
        :param symbol: Символ торговой пары, для которой требуется получить тикер.
        :param side: Сторона ('buy' или 'sell'), для которой требуется получить информацию о цене и объеме. По умолчанию None.
        :return: При указании side возвращает кортеж (цена, объем).
        Без side возвращает полный тикер с информацией о последней цене, объеме и других данных.
        """
        ticker = self.exchange.fetch_ticker(symbol)
        if side == 'buy':
            return ticker["ask"], ticker["askVolume"]
        elif side == 'sell':
            return ticker["bid"], ticker["bidVolume"]
        return ticker

    def get_ohlcv(self, symbol, timeframe, since=None, limit=None):
        """
        Возвращает исторические данные OHLCV (открытие, максимум, минимум, закрытие, объем)
        для заданной торговой пары и временного интервала. Позволяет указать начальное время
        и максимальное количество точек данных для возврата.
        :param symbol: Символ торговой пары, для которой требуется получить данные OHLCV.
        :param timeframe: Временной интервал для данных ('1m', '1h', '1d', '1M', '1y').
        :param since: Начальная метка времени для получения данных (в миллисекундах). По умолчанию None.
        :param limit: Количество возвращаемых точек данных. По умолчанию None.
        :return: list: Список данных OHLCV для указанной торговой пары и временного интервала.
        """
        return self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
