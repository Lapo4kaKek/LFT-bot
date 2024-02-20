import ccxt
from exchange.binance_exchange import BinanceExchange
from analysis.technical_analysis import TechnicalAnalysis
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

binance = BinanceExchange(api_key, api_secret)

order_book = binance.get_order_book('BTC/USDT')
print(order_book)
# example use
cost = binance.calculate_order_cost('BTC/USDT', 1, 'buy')
print(cost)

ta_binance = TechnicalAnalysis(binance, 'BTC/USDT')
print(ta_binance.get_ohlcv('1m', limit=1000))