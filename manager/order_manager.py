import requests
import logging

class OrderManager:
    @staticmethod
    async def place_buy_order(base_exchange, token_symbol, order_type, quantity, price=None):
        """
        Asynchronously places a buy order through the BaseExchange interface.
        """
        try:
            order_result = await base_exchange.place_order(token_symbol, "buy", order_type, quantity, price)
            return order_result
        except Exception as e:
            # Handle exceptions or errors from the BaseExchange
            print(f"Error placing buy order: {e}")
            return None

    @staticmethod
    async def place_sell_order(base_exchange, token_symbol, order_type, quantity, price=None):
        """
        Asynchronously places a sell order through the BaseExchange interface.
        """
        try:
            order_result = await base_exchange.place_order(token_symbol, "sell", order_type, quantity, price)
            return order_result
        except Exception as e:
            # Handle exceptions or errors from the BaseExchange
            print(f"Error placing sell order: {e}")
            return None