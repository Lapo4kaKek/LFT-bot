import ccxt
from exchange.binance_exchange import BinanceExchange
from exchange.bybit_exchange import BybitExchange
from exchange.hyperliquid_exchange import HyperLiquidExchange
from analysis.technical_analysis import TechnicalAnalysis
from dotenv import load_dotenv
import os
from utils.converter import Converter
from eth_utils import from_wei, to_hex
from eth_account.account import Account


load_dotenv()
#
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
# api_key_bybit = os.getenv('BYBIT_API_KEY')
# api_secret_bybit = os.getenv('BYBIT_API_SECRET')
#
# bybit = BybitExchange(api_key_bybit, api_secret_bybit)
# print(bybit.update_leverage("ARB", 2))
#
# # account = Account.from_key("")
# # print(account.address)
#
#
pkey = os.getenv('METAMASK_PKEY')
print(pkey)
client = HyperLiquidExchange(pkey)
print(client.get_leverage())
