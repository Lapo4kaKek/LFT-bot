from decimal import *


class Monitoring:
    def __init__(self, database):
        self.database = database

    def insert_orders_history_to_db(self, order_history):
        """
        Добавляет сразу несколько ордеров в кликхаус
        :param order_history: work in bybit only
        """
        data = []
        # print("Check:")
        # print(order_history['result']['list'])
        # Extract relevant data from each order
        for order in order_history['result']['list']:
            data.append((
                order['orderId'],
                order['symbol'],
                float(order['price']),
                float(order['qty']),
                order['side'],
                order['orderType'],
                order['orderStatus'],
                self.database.format_time_to_datetime(order['createdTime']),
                self.database.format_time_to_datetime(order['updatedTime'])
            ))

            # Define the column names in the same order as the data
            column_names = ['orderId', 'symbol', 'price', 'qty', 'side', 'order_type', 'order_status', 'created_time',
                            'updated_time']

            # Insert data into the database
            table_name = 'orders'  # Change this to your actual table name
            self.database.insert_data(table_name, data, column_names)

    def insert_single_order_to_db(self, order):
        """
        Adds a single order to ClickHouse
        :param order: order data (dictionary)
        """
        required_keys = ['orderId', 'exchange', 'symbol', 'price', 'qty', 'executedQty', 'totalCost', 'side',
                         'orderType',
                         'orderStatus', 'createdTime', 'updatedTime', 'commission', 'stopPrice']
        if not all(key in order for key in required_keys):
            print("Some required fields are missing in the order")
            return

        # Preparing data for insertion
        data = [(
            order['orderId'],  # order_id
            order['exchange'],  # exchange (binance or bybit)
            order['symbol'],  # symbol
            float(order['price']),  # price
            float(order['stopPrice']),  # stop loss price
            float(order['qty']),  # amount
            float(order['executedQty']),  # executedQty
            float(order['totalCost']),  # cost
            order['side'],  # side
            order['orderType'],  # order_type
            order['orderStatus'],  # order_status
            self.database.format_time_to_datetime(order['createdTime']),  # created_time
            self.database.format_time_to_datetime(order['updatedTime']),  # updated_time
            float(order['commission'])  # commission
        )]

        column_names = ['orderId', 'exchange', 'symbol', 'price', 'stopPrice', 'qty', 'executedQty', 'totalCost',
                        'side',
                        'orderType',
                        'orderStatus', 'createdTime', 'updatedTime', 'commission']

        table_name = 'orders'
        self.database.insert_data(table_name, data, column_names=column_names)

    def link_order_with_strategy(self, order_id, strategy_id):
        """
        Связывает ордер с стратегией в clickhouse.

        :param order_id: Идентификатор ордера.
        :param strategy_id: Идентификатор стратегии.
        """
        data = [(order_id, strategy_id)]

        column_names = ['orderId', 'strategyId']

        self.database.insert_data('order_strategy_link', data, column_names)

    def insert_strategy_info(self, strategy_info):
        """
        Добавляет информацию о стратегии в ClickHouse.
        :param strategy_info: Информация о стратегии в виде словаря.
        """
        data = [(
            strategy_info['strategyId'],
            strategy_info['name'],
            strategy_info['type'],
            strategy_info['exchange'],
            strategy_info['symbol'],
            float(strategy_info['balance']),
            float(strategy_info['assetsNumber']),
            strategy_info['openPositions'],
            strategy_info['status'],
            self.database.format_time_to_datetime(strategy_info['createdTime']),
            strategy_info['settings']
        )]

        column_names = ['strategyId', 'name', 'type', 'exchange', 'symbol', 'balance', 'assetsNumber', 'openPositions',
                        'status',
                        'createdTime', 'settings']

        self.database.insert_data('strategies', data, column_names)

    def get_strategy_info(self, strategy_id):
        """
        Ищет стратегию в ClickHouse.
        :param strategy_id: id стратегии.
        :return Dict, стратегия.
        """
        query = f"""
                SELECT * FROM strategies WHERE strategyId == '{strategy_id}' 
                """
        strategy = self.database.execute_query(query, columns=True)
        if strategy is not None:
            return strategy[0]
        return strategy

    def get_launched_strategies(self):
        """
        Ищет запущенные стратегии в ClickHouse.
        :return List, хранящий id стратегий.
        """
        query = f"""
                SELECT strategyId FROM strategies WHERE status == True 
                """
        strategies = self.database.execute_query(query, columns=True)
        return strategies

    def delete_strategy(self, strategy_id):
        """
        Удаляет стратегию по Id.
        :param strategy_id Id стратегии.
        :return List, хранящий id стратегий.
        """
        query = f"""
                DELETE FROM strategies WHERE strategyId = '{strategy_id}';
                """
        self.database.execute_query(query)

    def get_order_info(self, order_id):
        """
        Ищет ордер в ClickHouse.
        :param order_id: id ордера.
        :return Dict, ордер.
        """
        query = f"""
                SELECT * FROM orders WHERE orderId == '{order_id}' 
                """
        order = self.database.execute_query(query, columns=True)
        if order is not None:
            return order[0]
        return order

    def update_strategy_info(self, strategy_id, data):
        """
        Обновляет строку в таблице strategies по её id.
        :param strategy_id: id стратегии.
        :param data: Dict, данные для обновления нужных столбцов.
        :return Dict, стратегия.
        """
        condition = ', '.join([f"{key} = {data[key]}" for key in data])
        query = f"ALTER TABLE strategies UPDATE {condition} WHERE strategyId = '{strategy_id}'"
        self.database.execute_query(query)

    def update_order_info(self, order_id, data):
        """
        Обновляет строку в таблице orders по её id.
        :param order_id: id ордера.
        :param data: Dict, данные для обновления нужных столбцов.
        :return Dict, ордер.
        """
        condition = ', '.join([f"{key} = {data[key]}" for key in data])
        query = f"ALTER TABLE orders UPDATE {condition} WHERE orderId = '{order_id}'"
        self.database.execute_query(query)

    # нужно еще поработать над этим
    def calculate_and_insert_daily_pnl(self, orders_data, starting_capital):
        pnl_data = {}

        # Расчет PnL
        for order in orders_data:
            date = order['created_time']
            price = order['price']
            qty = order['qty']
            if order['side'] == 'Buy':
                pnl = -price * qty  # Покупка уменьшает PnL
            else:
                pnl = price * qty  # Продажа увеличивает PnL
            if date in pnl_data:
                pnl_data[date] += pnl
            else:
                pnl_data[date] = pnl

        for date, daily_pnl in pnl_data.items():
            self.database.insert_data(
                'daily_pnl',
                [(date, daily_pnl, daily_pnl / starting_capital * 100)],
                # starting_capital - это наш баланс
                ['date', 'daily_pnl', 'pnl_percentage']
            )

    def delete_all_data(self, table_name):
        return self.database.delete_all_data(table_name)

    def get_loss_order(self, strategy_id):
        try:
            query = f"""
                    SELECT TOP 1 orders.orderId
                    FROM order_strategy_link 
                    INNER JOIN orders ON orders.orderId = order_strategy_link.orderId 
                    WHERE order_strategy_link.strategyId = '{strategy_id}'
                    ORDER BY orders.createdTime DESC
                    """
            loss = self.database.execute_query(query)
            return loss[0][0]
        except Exception as err:
            return None

    def calculate_pnl_by_strategy(self, strategy_id):
        """
        Вычисляет PnL для заданной стратегии.
        """
        query = f"""
        SELECT 
            orderId, 
            exchange, 
            symbol, 
            price, 
            stopPrice,
            qty, 
            executedQty, 
            totalCost, 
            side, 
            orderType, 
            orderStatus, 
            createdTime, 
            updatedTime, 
            commission 
        FROM orders 
        INNER JOIN order_strategy_link ON orders.orderId = order_strategy_link.orderId 
        WHERE order_strategy_link.strategyId = '{strategy_id}'
        """

        orders = self.database.execute_query(query)

        total_cost = 0
        total_sell = 0
        total_qty = 0
        for order in orders:
            # Используйте индексы вместо ключей
            cost = float(order[7])  # Индекс для 'totalCost'
            qty = float(order[5])  # Индекс для 'qty'
            if order[4] != Decimal(0):  # Индекс для 'stopPrice'
                continue
            if order[8].lower() == 'buy':  # Индекс для 'side'
                total_cost += cost
                total_qty += qty
            elif order[8].lower() == 'sell':  # Индекс для 'side'
                total_sell += cost
                total_qty -= qty
        pnl = total_sell - total_cost

        return {
            'total_cost': total_cost,
            'total_sell': total_sell,
            'total_qty': total_qty,
            'pnl': pnl
        }
