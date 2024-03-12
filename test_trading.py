import os
from monitoring.monitoring import Monitoring
from dotenv import load_dotenv
import ccxt
from pprint import pprint
from asyncio import run
import ccxt.async_support as ccxt
from exchange.bybit_exchange import BybitExchange
import asyncio
from pybit.unified_trading import HTTP

load_dotenv()

api_key_bybit = os.getenv('BYBIT_API_KEY')
api_secret_bybit = os.getenv('BYBIT_API_SECRET')

api_key_binance = os.getenv('BINANCE_API_KEY')
api_secret_binance = os.getenv('BYBIT_API_SECRET')

async def main():


    client = ccxt.bybit({
        'apiKey': api_key_bybit,
        'secret': api_secret_bybit,
    })

    # client = ccxt.binance({
    #     'apiKey': api_key_binance,
    #     'secret': api_secret_binance,
    # })

    bybit = BybitExchange(api_key_bybit, api_secret_bybit)


    order = await client.create_market_buy_order_with_cost("STRK/USDT", 5)
    print(order)
    await asyncio.sleep(10)  # Пауза на 10 секунд

    order = await client.create_market_sell_order_with_cost("STRK/USDT", 4)
    print(order)

    await client.close()

#run(main())

bybit = BybitExchange(api_key_bybit, api_secret_bybit)
pprint(bybit.get_order_history(4))