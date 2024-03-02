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

    def get_order_book(self, coin, limit=None):
        """

        :param symbol: Символ торговой пары, для которой требуется получить стакан ордеров.
        :return: dict: Стакан ордеров для указанной торговой пары.
        """
        return super().get_order_book(coin, limit)


    def get_ticker(self, coin, side=None):
        """
        Возвращает информацию о последних ценах и объемах для заданной торговой пары.
        Может возвращать данные конкретно для покупки или продажи, если указан параметр side.
        :param symbol: Символ торговой пары, для которой требуется получить тикер.
        :param side: Сторона ('buy' или 'sell'), для которой требуется получить информацию о цене и объеме. По умолчанию None.
        :return: При указании side возвращает кортеж (цена, объем).
        Без side возвращает полный тикер с информацией о последней цене, объеме и других данных.
        """
        return super().get_ticker(coin, side)

    def get_ohlcv(self, coin, since=None, limit=None, timeframe='1m'):
        return super().get_ohlcv(coin, since, limit, timeframe)


    # you need add a parameters checker
    def create_order(self, coin, type, side, amount, price):
        """
        :param coin: Token name
        :param type: Market or Limit
        :param amount: Buy or Sell
        :param price:
        :return:
        """
        self.exchange.create_order(coin, type, side, amount, price)

    def get_balance(self):
        return super().get_balance()


    # futures
    def set_leverage(self, coin, level):
        return self.exchange.set_leverage(level, coin)

