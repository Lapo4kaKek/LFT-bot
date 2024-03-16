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

load_dotenv()

api_key_bybit = os.getenv('BYBIT_API_KEY')
api_secret_bybit = os.getenv('BYBIT_API_SECRET')

api_key_binance = os.getenv('BINANCE_API_KEY')
api_secret_binance = os.getenv('BINANCE_API_SECRET')

login_click = os.getenv('CLICKHOUSE_LOGIN')
password_click = os.getenv('CLICKHOUSE_PASSWORD')
port = os.getenv('CLICKHOUSE_PORT')
async def example_binance_work():
    monitoring = Monitoring('localhost', 8123, login_click, password_click)

    binance = BinanceExchange(api_key_binance, api_secret_binance, monitoring)

    order = binance.create_market_sell_order("STRK/USDT", 2.3)

    print(order)

async def main():
    monitoring = Monitoring('localhost', port, login_click, password_click)

    bybit = BybitExchange(api_key_bybit, api_secret_bybit, monitoring)
    binance = BinanceExchange(api_key_binance, api_secret_binance, monitoring)

    order1 = bybit.create_market_buy_order("STRK/USDT", 2)
    print(order1)

    order2 = binance.create_market_buy_order("STRK/USDT", 2.3)
    order3 = bybit.create_market_sell_order("STRK/USDT", 2)

    order4 = binance.create_market_sell_order("STRK/USDT", 2.3)
    print(order2)
    print(order3)
    print(order4)


    return



run(main())