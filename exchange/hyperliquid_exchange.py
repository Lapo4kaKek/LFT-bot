import constans
from .base_exchange import BaseExchange
import ccxt
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from eth_account.account import Account
from hyperliquid.info import Info
# from hyperliquid.utils import constants
import constans
import json
from hyperliquid.exchange import Exchange
import requests
from typing import Any, Dict

# Work in arbitrum network
class HyperLiquidExchange(BaseExchange):
    def __init__(self, privateKey):
        self.api_secret = privateKey
        # self.manager = HyperLiquidManager(Account.from_key(self.api_secret))
        self.account = Account.from_key(self.api_secret)
        self.info = Info("https://api.hyperliquid.xyz", skip_ws=True)
        self.exchange = Exchange(self.account, "https://api.hyperliquid.xyz")
        super().__init__(api_key=None, api_secret=privateKey)

    def post(self, endpoint: str, payload: Dict[str, Any]) -> Any:
        """Отправить POST запрос к API.

        Args:
            endpoint (str): конечная точка API, к которой будет выполнен запрос.
            payload (Dict[str, Any]): тело запроса в формате словаря Python.

        Returns:
            Any: Ответ от сервера.
        """
        url = f"{endpoint}"
        headers = {'Content-Type': 'application/json', 'Content-Length': '<calculated when request is sent>'}
        print(headers)
        print(payload)
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Ошибка запроса: {response.status_code}, {response.text}")

        return response.json()

    def send_rpc_request(self, url, method, params):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        print(url)
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()  # return json response

    def get_balance(self, api_url = constans.ARBITRUM_MAINNET):
        address = self.get_address()
        print(address)
        response_json = self.send_rpc_request(api_url, "eth_getBalance", [address, "latest"])
        balance_hex = response_json['result']

        return balance_hex

    def get_address(self):
        return self.account.address

    # work
    def get_user_state(self):
        return self.info.user_state(self.account.address)

    # work
    def get_leverage(self, order_number=0):
        user_state = self.get_user_state()
        try:
            return user_state["assetPositions"][order_number]["position"]["leverage"]["value"]
        except (IndexError, KeyError):
            return "Information not available"

    # work
    def update_leverage(self, leverage, coin, is_cross=True):
        return self.exchange.update_leverage(leverage, coin, is_cross)

    # the same 'update leverage'
    def set_leverage(self, leverage, coin):
        return self.exchange.update_leverage(leverage, coin, True)

    # Gtc - Good Till Canceled
    # work
    def __place_long_order(self, coin, amount, price):
        return self.exchange.order(coin, True, amount, price, {"limit": {"tif": "Gtc"}})

    # Gtc - Good Till Canceled
    # work
    def __place_short_order(self, coin, amount, price):
        return self.exchange.order(coin, False, amount, price, {"limit": {"tif": "Gtc"}})
    # work
    def __place_long_market_buy_order(self, coin, size):
        is_buy = True
        return self.exchange.market_open(coin, is_buy, size, None)

    # work
    def __place_short_market_buy_order(self, coin, size):
        is_buy = False
        return self.exchange.market_open(coin, is_buy, size, None)


    # work
    def close_market_order(self, coin, size):
        return self.exchange.market_close(coin, size)

    # work
    def cancel_order(self, coin, order_id):
        return self.exchange.cancel(coin, order_id)

    # work
    def get_funding_rate(self, coin, start):
        return self.info.funding_history(coin, start)

    # work
    def get_current_funding_rate(self, coin):
        current_time = int(time.time() * 1000)  # Текущее время в миллисекундах
        one_hour_ago = current_time - 60 * 60 * 1000
        return self.info.funding_history(coin, one_hour_ago, current_time)

    # work
    def get_user_funding(self, start_time):
        return self.info.post("/info", {"type": "userFunding", "user": self.account.address, "startTime": start_time})
        # return self.post(constants.MAINNET_API_URL + "/info", {"type": "userState", "user": self.account.address, "startTime": start_time})

    # work
    def user_state(self, start_time):
        # Здесь мы отправляем запрос на получение состояния пользователя, а не истории фандинга.
        return self.post(constans.HYPERLIQUID_MAIN_API_URL + "/info",
                         {"type": "userState", "user": self.account.address, "startTime": start_time})


    # work
    def calculate_funding_impact(self, open_time, position_size, position_side):
        current_time = int(time.time() * 1000)

        funding_history = self.info.funding_history('BTC', open_time, current_time)

        total_funding_fee = 0

        for funding_event in funding_history:
            if funding_event['time'] >= open_time:
                funding_fee = position_size * funding_event['fundingRate']
                if position_side == 'long':
                    total_funding_fee -= funding_fee
                else:
                    total_funding_fee += funding_fee

        return total_funding_fee

    def create_order(self, coin, type, side, amount, price=None):
        if type == "MARKET":
            if side == "BUY":
                return self.__place_long_market_buy_order(coin, amount)
            elif side == "SELL": # i think maybe here need close_market
                return self.__place_short_market_buy_order(coin, amount)
        elif type == "LIMIT":
            if side == "BUY":
                return self.__place_long_order(coin, amount, price)
            elif side == "SELL": # i think maybe here need close_market
                return self.__place_short_order(coin, amount, price)
        else:
            raise ValueError("Invalid order type or side")



    #############################

    def create_market_buy_order(self, symbol, order_size):
        return self.__place_long_market_buy_order(symbol, order_size)

    def create_market_sell_order(self, symbol, order_size):
        return self.__place_short_market_buy_order(symbol, order_size)