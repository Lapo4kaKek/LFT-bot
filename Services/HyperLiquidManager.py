from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
from hyperliquid.info import Info
from hyperliquid.utils import constants
import utils
import eth_account
from eth_abi import encode
from eth_account.signers.local import LocalAccount
from eth_utils import keccak, to_hex
from eth_account.signers.local import LocalAccount
from hyperliquid.utils.constants import TESTNET_API_URL
from hyperliquid.exchange import Exchange
from constans import MAINNET_API_URL
import datetime
from typing import Any, Dict
import requests

class HyperLiquidManager:
    def __init__(self, account, api_url):
        self.account = account
        self.info = Info(api_url, skip_ws=True)
        self.exchange = Exchange(account, api_url)

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

    def get_user_state(self):
        return self.info.user_state(self.account.address)

    def get_leverage(self, order_number=0):
        user_state = self.get_user_state(self.account.address)
        try:
            return user_state["assetPositions"][order_number]["position"]["leverage"]["value"]
        except (IndexError, KeyError):
            return "Information not available"

    def update_leverage(self, leverage, coin, is_cross=True):
        return self.exchange.update_leverage(leverage, coin, is_cross)

    # Gtc - Good Till Canceled
    def place_long_order(self, coin, amount, price):
        return self.exchange.order(coin, True, amount, price, {"limit": {"tif": "Gtc"}})

    # Gtc - Good Till Canceled
    def place_short_order(self, amount, price):
        return self.exchange.order("ETH", False, amount, price, {"limit": {"tif": "Gtc"}})
    # work
    def place_long_market_buy_order(self, coin, size):
        is_buy = True
        return self.exchange.market_open(coin, is_buy, size, None)
    # work
    def place_short_market_buy_order(self, coin, size):
        is_buy = False
        return self.exchange.market_open(coin, is_buy, size, None)
    # work
    def close_market_order(self, coin, size):
        return self.exchange.market_close(coin, size)
    def cancel_order(self, coin, order_id):
        return self.exchange.cancel(coin, order_id)

    def get_funding_rate(self, coin, start):
        return self.info.funding_history(coin, start)

    def get_current_funding_rate(self, coin):
        current_time = int(time.time() * 1000)  # Текущее время в миллисекундах
        one_hour_ago = current_time - 60 * 60 * 1000
        return self.info.funding_history(coin, one_hour_ago, current_time)

    def get_user_funding(self, start_time):
        return self.info.post("/info", {"type": "userFunding", "user": self.account.address, "startTime": start_time})
        # return self.post(constants.MAINNET_API_URL + "/info", {"type": "userState", "user": self.account.address, "startTime": start_time})

    def user_state(self, start_time):
        # Здесь мы отправляем запрос на получение состояния пользователя, а не истории фандинга.
        return self.post(constants.MAINNET_API_URL + "/info",
                         {"type": "userState", "user": self.account.address, "startTime": start_time})

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

