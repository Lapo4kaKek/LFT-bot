# from .base_exchange import BaseExchange
# import ccxt
# from eth_account import Account
# from http.server import HTTPServer, BaseHTTPRequestHandler
#
# class HyperLiquidExchange(BaseExchange):
#     def __init__(self, privateKey, secret):
#
#
#     def get_order_book(self, coin, limit=None):
#         return self.exchange.fetch_order_book(coin, limit)
#
#     def get_ohlcv(self, coin, since=None, limit=None, timeframe='1m'):
#         params = {}
#         if since is not None:
#             params['since'] = since
#         if limit is not None:
#             params['limit'] = limit
#
#         return self.exchange.fetch_ohlcv(coin, timeframe, **params)
#
#     # you need add a parameters checker
#     def create_order(self, coin, type, side, amount, price):
#         """
#         :param coin: Token name
#         :param type: Market or Limit
#         :param amount: Buy or Sell
#         :param price:
#         :return: order_id?
#         """
#         self.exchange.create_order(coin, type, side, amount, price)
#
