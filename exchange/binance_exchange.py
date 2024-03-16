import ccxt
from .base_exchange import BaseExchange
from monitoring.monitoring import Monitoring
from datetime import datetime
from utils.converter import Converter

class BinanceExchange(BaseExchange):
    """
    Предоставляет специализированные методы для работы с криптовалютной биржей Binance.
    """
    def __init__(self, api_key, api_secret, monitoring):
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
        self.monitoring = monitoring

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
    def create_order(self, coin, type, side, amount, price=None):
        """
        :param coin: Token name
        :param type: Market or Limit
        :param amount: Buy or Sell
        :param price:
        :return:
        """
        if price is not None:
            return self.exchange.create_order(coin, type, side, amount, price)
        return self.exchange.create_order(coin, type, side, amount)

    def get_balance(self):
        return super().get_balance()


    # futures
    def set_leverage(self, coin, level):
        return self.exchange.set_leverage(level, coin)


    # work
    def create_market_buy_order(self, symbol, order_size):
        result = self.exchange.create_order(symbol, 'market', 'buy', order_size)
        print(result)
        if result is not None:
            order_stm = self.parse_order_to_clickhouse_format(result)
            self.monitoring.insert_single_order_to_db(order_stm)
            return result
        return result

    # work
    def create_market_sell_order(self, symbol, order_size):
        result = self.exchange.create_order(symbol, 'market', 'sell', order_size)
        print(result)
        if result is not None:
            order_stm = self.parse_order_to_clickhouse_format(result)
            self.monitoring.insert_single_order_to_db(order_stm)
            return result
        return result

    def format_time_to_datetime(self, timestamp_str):
        if timestamp_str.isdigit():
            return datetime.fromtimestamp(int(timestamp_str) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

    def parse_order_to_clickhouse_format(self, order):
        info = order['info']
        executed_qty = float(info.get('executedQty', 0))
        cummulative_quote_qty = float(info.get('cummulativeQuoteQty', 0))
        commission = 0.0
        commission_asset = ''
        fills = info.get('fills', [])
        if fills:
            fill = fills[0]
            commission = float(fill.get('commission', '0'))
            commission_asset = fill.get('commissionAsset', '')

        parsed_order = {
            'orderId': info['orderId'],
            'exchange': 'binance',
            'symbol': info['symbol'],
            'price': float(fills[0]['price']) if fills else 0.0,
            # Берем цену из первого заполнения, если оно существует
            'qty': float(info['origQty']),
            'executedQty': executed_qty,
            'totalCost': cummulative_quote_qty,
            'side': info['side'],
            'orderType': info['type'],
            'orderStatus': info['status'],
            'createdTime': info['workingTime'],
            'updatedTime': info['workingTime'],
            'commission': commission,
            #'commission_asset': commission_asset,
            #'average_price': cummulative_quote_qty / executed_qty if executed_qty > 0 else 0
        }
        print(parsed_order)

        return parsed_order



