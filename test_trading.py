import os
from monitoring.monitoring import Monitoring
from dotenv import load_dotenv
import ccxt
from pprint import pprint
from asyncio import run
import ccxt.async_support as ccxt
from exchange.bybit_exchange import BybitExchange
import asyncio

load_dotenv()

async def main():
    api_key_bybit = os.getenv('BYBIT_API_KEY')
    api_secret_bybit = os.getenv('BYBIT_API_SECRET')

    client = ccxt.bybit({
        'apiKey': api_key_bybit,
        'secret': api_secret_bybit,
    })
    bybit = BybitExchange(api_key_bybit, api_secret_bybit)
    # print(client.set_leverage(2, "STRK/USDT:USDT"))

    print(bybit.set_leverage("STRKUSDT", 2))

    print(client.load_markets())
    order = await client.create_order('STRKUSDT', "market", "buy", 6)
    print(order)
    await asyncio.sleep(10)
    response = await client.cancel_order(order['id'], order['symbol'])
    print(response)


api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
run(main())