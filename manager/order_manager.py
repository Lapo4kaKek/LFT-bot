import requests
import logging
from decimal import *


class OrderManager:
    @staticmethod
    async def place_buy_order(strategy_id, monitoring, exchange, token_symbol, balance, stop_loss=None):
        """
        Создаёт ордер на покупку.
        """
        try:
            ticker = await exchange.get_ticker(token_symbol, 'buy')
            order = await exchange.create_market_buy_order(strategy_id=strategy_id, symbol=token_symbol,
                                                           order_size=Decimal(
                                                               balance) / Decimal(
                                                               ticker[0]))
            await monitoring.update_strategy_info(strategy_id=strategy_id,
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
        try:
            monitoring.get_loss_order(strategy_id)
            order = await exchange.create_market_sell_order(strategy_id=strategy_id, symbol=token_symbol,
                                                            order_size=order_size)
            await monitoring.update_strategy_info(strategy_id=strategy_id,
                                                  data={'balance': Decimal(balance) + Decimal(order['cost']), 'assetsNumber': Decimal(0),
                                                        'openPositions': False})

            return order
        except Exception as e:
            print(f"Error placing sell order: {e}")
            return None
