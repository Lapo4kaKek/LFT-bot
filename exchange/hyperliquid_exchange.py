import constans
from .base_exchange import BaseExchange
from Services.HyperLiquidManager import HyperLiquidManager
import ccxt
from http.server import HTTPServer, BaseHTTPRequestHandler
from eth_account.account import Account


# Work in arbitrum network
class HyperLiquidExchange(BaseExchange):
    def __init__(self, privateKey):
        super().__init__(api_key=None, api_secret=privateKey)

    def get_order_book(self, coin, limit=None):
        return self.exchange.fetch_order_book(coin, limit)

    def get_ohlcv(self, coin, since=None, limit=None, timeframe='1m'):
        params = {}
        if since is not None:
            params['since'] = since
        if limit is not None:
            params['limit'] = limit

        return self.exchange.fetch_ohlcv(coin, timeframe, **params)

    # you need add a parameters checker
    def create_order(self, coin, type, side, amount, price):
        """
        :param coin: Token name
        :param type: Market or Limit
        :param amount: Buy or Sell
        :param price:
        :return: order_id?
        """
        self.exchange.create_order(coin, type, side, amount, price)

    # not implement, this need decoded pKey -> address

    def get_balance(self):
        print(self.api_secret)
        manager = HyperLiquidManager(Account.from_key(self.api_secret))
        print("done manager create")
        address = manager.get_address()
        print(address)
        params = [address, "latest"]

        return manager.send_rpc_request(constans.ARBITRUM_MAINNET, "eth_getBalance", params)
