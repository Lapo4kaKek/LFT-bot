import requests
import logging


class OrderManager:
    @staticmethod
    async def place_buy_order(strategy_id, monitoring, base_exchange, token_symbol, order_size, stop_loss=None):
        """
        Создаёт ордер на покупку.
        """
        try:
            order = await base_exchange.create_market_buy_order(strategy_id=strategy_id, symbol=token_symbol, order_size=order_size)
            await monitoring.update_strategy_info(strategy_id=strategy_id,
                                                  data={'assetsNumber': order['filled'], 'openPositions': True})
            if stop_loss:
                stop_loss_order = await base_exchange.create_market_stop_loss_order(strategy_id=strategy_id, symbol=token_symbol,
                                                                                    order_size=order['filled'],
                                                                                    params=stop_loss)
            return order
        except Exception as e:
            print(f"Error placing buy order: {e}")
            return None

    @staticmethod
    async def place_sell_order(strategy_id, monitoring, base_exchange, token_symbol, order_size):
        """
        Создаёт ордер на продажу.
        """
        try:
            order = await base_exchange.create_market_sell_order(strategy_id=strategy_id, symbol=token_symbol, order_size=order_size)
            await monitoring.update_strategy_info(strategy_id=strategy_id,
                                                  data={'assetsNumber': order['filled'],
                                                        'openPositions': False})

            return order
        except Exception as e:
            print(f"Error placing sell order: {e}")
            return None
