import ccxt
from exchange.binance_exchange import BinanceExchange
from analysis.technical_analysis import TechnicalAnalysis
from dotenv import load_dotenv
import os
from exchange.bybit_exchange import BybitExchange

load_dotenv()
#
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
#
binance = BinanceExchange(api_key, api_secret)
#
# # example use
# print(binance.get_ohlcv('BTC/USDT'))
# print(binance.get_ticker('BTC/USDT', 'buy'))
# print(TechnicalAnalysis(binance, 'BTC/USDT').get_ohlcv('1m', limit=1000))

api_key_bybit = os.getenv('BYBIT_API_KEY')
api_secret_bybit = os.getenv('BYBIT_API_SECRET')

bybit = BybitExchange(api_key_bybit, api_secret_bybit)
print(bybit.get_ohlcv('ETH/USDT'))