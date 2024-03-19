import os
from monitoring.monitoring import Monitoring
from dotenv import load_dotenv
import ccxt
from pprint import pprint
from asyncio import run
#import ccxt.async_support as ccxt
from exchange.bybit_exchange import BybitExchange
import asyncio
from pybit.unified_trading import HTTP
from exchange.binance_exchange import BinanceExchange
import hashlib
import hmac
import json
import requests
import urllib3
import time
from urllib.parse import quote_plus
import time

load_dotenv()

api_key_bybit = os.getenv('BYBIT_API_KEY')
api_secret_bybit = os.getenv('BYBIT_API_SECRET')

api_key_bybit2 = os.getenv('BYBIT_API_KEY2')
api_secret_bybit2 = os.getenv('BYBIT_API_SECRET2')

api_key_binance = os.getenv('BINANCE_API_KEY')
api_secret_binance = os.getenv('BINANCE_API_SECRET')

login_click = os.getenv('CLICKHOUSE_LOGIN')
password_click = os.getenv('CLICKHOUSE_PASSWORD')
port = os.getenv('CLICKHOUSE_PORT')

monitoring = Monitoring('localhost', port, login_click, password_click)

bybit = BybitExchange(api_key_bybit, api_secret_bybit, monitoring)
binance = BinanceExchange(api_key_binance, api_secret_binance, monitoring)

async def example_binance_work():
    monitoring = Monitoring('localhost', 8123, login_click, password_click)

    binance = BinanceExchange(api_key_binance, api_secret_binance, monitoring)

    order = binance.create_market_sell_order("STRK/USDT", 2.3)

    print(order)

async def main():
    order1 = bybit.create_market_buy_order("STRK/USDT", 2)
    print(order1)

    order2 = binance.create_market_buy_order("STRK/USDT", 2.3)
    order3 = bybit.create_market_sell_order("STRK/USDT", 2)

    order4 = binance.create_market_sell_order("STRK/USDT", 2.3)
    print(order2)
    print(order3)
    print(order4)


    return

async def testnet():
    order = bybit.create_market_buy_order_native("ETHUSDT", 1, True)

async def get_order_list():
    api_key = api_key_bybit2
    secret_key = api_secret_bybit2
    httpClient = requests.Session()
    recv_window = str(5000)
    url = "https://api.bybit.com"  # Testnet endpoint

    def HTTP_Request(endPoint, method, payload, Info):
        global time_stamp
        time_stamp = str(int(time.time() * 10 ** 3))
        signature = genSignature(payload)
        headers = {
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': recv_window,
            'Content-Type': 'application/json'
        }
        if (method == "POST"):
            response = httpClient.request(method, url + endPoint, headers=headers, data=payload)
        else:
            response = httpClient.request(method, url + endPoint + "?" + payload, headers=headers)
        print(response.text)
        print(Info + " Response Time : " + str(response.elapsed))

    def genSignature(payload):
        param_str = str(time_stamp) + api_key + recv_window + payload
        hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        return signature


    # Get Order List
    endpoint = "/spot/v3/private/order"
    method = "GET"
    params = 'orderLinkId=18f2f7a4259843ba9a06ccf577a54c2a'
    HTTP_Request(endpoint, method, params, "List")


# run(testnet())
if __name__ == '__main__':
    # Измеряем время выполнения первой функции
    start_time = time.time()
    bybit.create_market_buy_order("STRK/USDT", 1.05)
    end_time = time.time()
    print(f"Time ccxt: {end_time - start_time} sec")

    # database.delete_all_data("orders")
    start_time = time.time()
    bybit.create_market_buy_order_native("STRKUSDT", 2)
    end_time = time.time()
    print(f"Time native: {end_time - start_time} sec")

