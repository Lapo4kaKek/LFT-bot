import os
from monitoring.monitoring import Monitoring
from dotenv import load_dotenv
import ccxt

from exchange.bybit_exchange import BybitExchange
# import ccxt
# from exchange.binance_exchange import BinanceExchange
# from exchange.hyperliquid_exchange import HyperLiquidExchange
# from analysis.technical_analysis import TechnicalAnalysis

#
# from utils.converter import Converter
# from eth_utils import from_wei, to_hex
# from eth_account.account import Account

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
#
# binance = BinanceExchange(api_key, api_secret)
# #
# # # example use
# # print(binance.get_ohlcv('BTC/USDT'))
# # print(binance.get_ticker('BTC/USDT', 'buy'))
# # print(TechnicalAnalysis(binance, 'BTC/USDT').get_ohlcv('1m', limit=1000))
#
api_key_bybit = os.getenv('BYBIT_API_KEY')
api_secret_bybit = os.getenv('BYBIT_API_SECRET')

client = ccxt.bybit({
    'apiKey': api_key_bybit,
    'secret': api_secret_bybit,
})
bybit = BybitExchange(api_key_bybit, api_secret_bybit)
# print(bybit.set_leverage("STRKUSDT", 1))

client.load_markets()
#print(client.set_leverage(3, "STRKUSDT"))
#print(client.create_order('STRKUSDT', "market", "buy", 6))
print(client.cancel_order('d68001a7-2a56-4efe-b6e7-c1f6fd8117ad', "STRK/USDT:USDT"))


login_click = os.getenv('CLICKHOUSE_LOGIN')
password_click = os.getenv('CLICKHOUSE_PASSWORD')

# monitoring = Monitoring('localhost', 8123, login_click, password_click)
#
# monitoring.fetch_and_print_table_data("example_table")
