import os
import uuid
from _decimal import Decimal
from database.database import Database
from monitoring.monitoring import Monitoring
from dotenv import load_dotenv
import ccxt
from pprint import pprint
from asyncio import run
# import ccxt.async_support as ccxt
from exchange.bybit_exchange import BybitExchange
import asyncio
from pybit.unified_trading import HTTP
from exchange.binance_exchange import BinanceExchange
from strategy import macd_strategy
from loguru import logger

load_dotenv()

# api_key_bybit = os.getenv('BYBIT_API_KEY')
# api_secret_bybit = os.getenv('BYBIT_API_SECRET')

api_key_bybit = os.getenv('BYBIT_API_TESTNET')
api_secret_bybit = os.getenv('BYBIT_API_SECRET_TESTNET')

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


async def macd_trading(bybit, monitoring):
    strategy_id = str(uuid.uuid4())

    bybit.exchange.verbose = True
    strategy1 = macd_strategy.MACDStrategy(exchange=bybit, symbol="BTCUSDT",
                                                  settings={'strategy_name': 'Strategy 1',
                                                            'filter_days': 3, 'limit': 100, 'loss_coef': 0.8},
                                           strategy_id=strategy_id, monitoring=monitoring)
    logger.info("Init strategy MACD")

    logger.info(f"Strategy with ID: {strategy_id} and parameters: {strategy1.settings} ready and running!")

    # Запуск торговли для всех стратегий
    await asyncio.gather(
        strategy1.trading(),
    )


async def main():
    print("Start:")
    database = Database('localhost', port, login_click, password_click)
    monitoring = Monitoring(database)
    bybit = BybitExchange(api_key_bybit, api_secret_bybit, monitoring)
    bybit.exchange.set_sandbox_mode(True)

    # await macd_trading(bybit, monitoring)
    #pnl_result = monitoring.calculate_pnl_by_strategy("d99ac788-8b7e-4061-8a50-cc1b06fe0754")
    #print(f"{pnl_result['pnl']}")
    # monitoring.delete_all_data("strategies")
    # monitoring.delete_all_data("order_strategy_link")
    await macd_trading(bybit, monitoring)


#run(main())
database = Database('localhost', port, login_click, password_click)
monitoring = Monitoring(database)
monitoring.delete_all_data("order_strategy_link")
monitoring.delete_all_data("orders")
monitoring.delete_all_data("pnl_data")
monitoring.delete_all_data("strategies")