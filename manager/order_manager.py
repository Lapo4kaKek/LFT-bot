import requests
import logging
from loguru import logger

class OrderManager:
    @staticmethod
    async def place_buy_order(base_exchange, token_symbol, order_type, quantity, price=None):
        """
        Asynchronously places a buy order through the BaseExchange interface.
        """
        logger.info(f"Placing sell order: Symbol={token_symbol}, Type={order_type}, Quantity={quantity}, Price={price}")
        try:
            order_result = await base_exchange.place_order(token_symbol, "buy", order_type, quantity, price)
            logger.info(f"Buy order placed successfully: {order_result}")
            return order_result
        except Exception as e:
            # Handle exceptions or errors from the BaseExchange
            # print(f"Error placing buy order: {e}")
            logger.error(f"Error placing buy order: {e}")
            return None

    @staticmethod
    async def place_sell_order(base_exchange, token_symbol, order_type, quantity, price=None):
        """
        Asynchronously places a sell order through the BaseExchange interface.
        """
        logger.info(f"Placing sell order: Symbol={token_symbol}, Type={order_type}, Quantity={quantity}, Price={price}")
        try:
            order_result = await base_exchange.place_order(token_symbol, "sell", order_type, quantity, price)
            logger.info(f"Sell order placed successfully: {order_result}")
            return order_result
        except Exception as e:
            # Handle exceptions or errors from the BaseExchange
            logger.error(f"Error placing sell order: {e}")
            return None