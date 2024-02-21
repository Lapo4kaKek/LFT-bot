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
ta = TechnicalAnalysis(binance, 'BTC/USDT')

# OHLCV
print(ta.get_ohlcv('1d', limit=1000))

# RSI
print("RSI:", ta.get_rsi().to_dict())

# MACD
macd, signal = ta.get_macd()
print("MACD:", macd.to_dict())
print("Signal line:", signal.to_dict())

# Aroon
aroon_up, aroon_down = ta.get_aroon()
print("Aroon Up:", aroon_up.to_dict())
print("Aroon Down:", aroon_down.to_dict())

# OBV
print("OBV:", dict(ta.get_obv()))

# Stochastic Oscillator
stoch_k, stoch_d = ta.get_stochastic_oscillator()
print("Stochastic %K:", stoch_k.to_dict())
print("Stochastic %D:", stoch_d.to_dict())

# SMA
print("SMA:", dict(ta.get_sma()))

# EMA
print("EMA:", dict(ta.get_ema()))

# Bollinger Bands
upper_band, sma, lower_band = ta.get_bollinger_bands()
print("Upper Bollinger Band:", upper_band.to_dict())
print("Middle Bollinger Band (SMA):", sma.to_dict())
print("Lower Bollinger Band:", lower_band.to_dict())

# Momentum
print("Momentum:", dict(ta.get_momentum()))