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
                         'orderStatus', 'createdTime', 'updatedTime', 'commission']
        if not all(key in order for key in required_keys):
            print("Some required fields are missing in the order")
            return

        # Preparing data for insertion
        data = [(
            order['orderId'],  # order_id
            order['exchange'],  # exchange (binance or bybit)
            order['symbol'],  # symbol
            float(order['price']),  # price
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

        column_names = ['orderId', 'exchange', 'symbol', 'price', 'qty', 'executedQty', 'totalCost', 'side',
                        'orderType',
                        'orderStatus', 'createdTime', 'updatedTime', 'commission']

        table_name = 'orders'
        self.database.insert_data(table_name, data, column_names=column_names)

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
