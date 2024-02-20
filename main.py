import ccxt
from exchange.binance_exchange import BinanceExchange
from analysis.technical_analysis import TechnicalAnalysis
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

binance = BinanceExchange(api_key, api_secret)

# example use
print(binance.get_order_book('BTC/USDT'))
print(binance.get_ticker('BTC/USDT', 'buy'))
print(TechnicalAnalysis(binance, 'BTC/USDT').get_ohlcv('1m', limit=1000))