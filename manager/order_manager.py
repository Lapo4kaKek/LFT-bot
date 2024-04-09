import asyncio

import requests
import logging
from decimal import *


class OrderManager:
    @staticmethod
    async def place_buy_order(strategy_id, monitoring, exchange, token_symbol, balance, stop_loss=None):
        """
        Создаёт ордер на покупку.
        """
        lock = asyncio.Lock()
        async with lock:
            try:
                ticker = await exchange.get_ticker(token_symbol, 'buy')
                order = await exchange.create_market_buy_order(strategy_id=strategy_id, symbol=token_symbol,
                                                               order_size=Decimal(
                                                                   balance) / Decimal(
                                                                   ticker[0]))
                monitoring.update_strategy_info(strategy_id=strategy_id,
                                                      data={'balance': balance - Decimal(order['cost']),
                                                            'assetsNumber': order['filled'], 'openPositions': True})
                if stop_loss is not None:
                    stop_loss_order = await exchange.create_market_stop_loss_order(strategy_id=strategy_id,
                                                                                   symbol=token_symbol,
                                                                                   order_size=order['filled'],
                                                                                   params={
                                                                                       'triggerPrice': Decimal(
                                                                                           ticker[0]) * Decimal(
                                                                                           stop_loss)
                                                                                   })
                return order
            except Exception as e:
                print(f"Error placing buy order: {e}")
                return None

    @staticmethod
    async def place_sell_order(strategy_id, monitoring, exchange, token_symbol, balance, order_size):
        """
        Создаёт ордер на продажу.
        """
        lock = asyncio.Lock()
        async with lock:
            try:
                loss_id = monitoring.get_loss_order(strategy_id)
                if loss_id is not None:
                    await exchange.cancel_order(loss_id, token_symbol)
                monitoring.update_order_info(order_id=loss_id,
                                                   data={'orderStatus': '\'closed\''})
                order = await exchange.create_market_sell_order(strategy_id=strategy_id, symbol=token_symbol,
                                                                order_size=order_size)
                monitoring.update_strategy_info(strategy_id=strategy_id,
                                                      data={'balance': Decimal(balance) + Decimal(order['cost']),
                                                            'assetsNumber': Decimal(0),
                                                            'openPositions': False})

                return order
            except Exception as e:
                print(f"Error placing sell order: {e}")
                return None

    @staticmethod
    async def check_loss_order(strategy_id, monitoring, exchange, token_symbol, balance):
        """
        Проверяет статус стоп-лосс ордера.
        """
        lock = asyncio.Lock()
        async with lock:
            try:
                loss_id = monitoring.get_loss_order(strategy_id)
                strategy = monitoring.get_strategy_info(strategy_id)
                if loss_id is not None:
                    order = await exchange.fetch_loss_order(loss_id, token_symbol)
                    if order['status'] == 'closed' and strategy['openPositions'] == True:
                        monitoring.update_order_info(order_id=loss_id,
                                                           data={'orderStatus': '\'closed\'',
                                                                 'executedQty': order['filled'],
                                                                 'price': order['price']})
                        monitoring.update_strategy_info(strategy_id=strategy_id,
                                                              data={'balance': Decimal(balance) + Decimal(order['cost']),
                                                                    'assetsNumber': Decimal(0),
                                                                    'openPositions': False})
            except Exception as e:
                print(f"Error checking loss order: {e}")
                return None