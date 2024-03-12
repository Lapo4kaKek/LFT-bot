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

    api_key_binance = os.getenv('BINANCE_API_KEY')
    api_secret_binance = os.getenv('BYBIT_API_SECRET')

    # client = ccxt.bybit({
    #     'apiKey': api_key_bybit,
    #     'secret': api_secret_bybit,
    # })

    client = ccxt.binance({
        'apiKey': api_key_binance,
        'secret': api_secret_binance,
    })

    bybit = BybitExchange(api_key_bybit, api_secret_bybit)
    # print(client.set_leverage(2, "STRK/USDT:USDT"))

    #print(bybit.set_leverage("STRKUSDT", 2))


    order = await bybit.create_market_buy_order("STRK/USDT", 3)
    print(order)
    await asyncio.sleep(10)
    response = await bybit.create_market_sell_order("STRK/USDT", 3)
    print(response)

    # Закрытие асинхронного клиента после выполнения всех операций
    await client.close()



api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
run(main())