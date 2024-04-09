import clickhouse_connect
from datetime import datetime
from loguru import logger

class Database:
    def __init__(self, host='localhost', port=8123, username='default', password=''):
        self.client = clickhouse_connect.get_client(host=host, port=port, username=username, password=password)
        logger.info(f"ClickHouse client initialized with host={host}, port={port}, username={username}")

    def create_table(self, table_name, columns):
        columns_with_types = ', '.join([f'{name} {type}' for name, type in columns.items()])
        create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types}) ENGINE = MergeTree() ORDER BY tuple()'
        self.client.command(create_table_query)
        logger.info(f"Table {table_name} created or already exists")

    def delete_all_data(self, table_name):
        '''
        Удаляет все данные из таблицы
        :param table_name: название таблицы
        :return:
        '''
        create_table_query = f'TRUNCATE TABLE {table_name}'
        self.client.command(create_table_query)
        logger.info(f"All data from table {table_name} deleted")

    def insert_data(self, table_name, data, column_names=None):
        result = self.client.insert(table_name, data, column_names=column_names)
        logger.info(f"Inserted data into table {table_name}: {data} with result: {result}")
        return result

    def fetch_and_print_table_data(self, table_name):
        result = self.client.query(f'SELECT * FROM {table_name}')
        for row in result.result_rows:
            print(row)
        logger.info(f"Fetched data from table {table_name}")

    def format_time_to_datetime(self, timestamp_str):
        return datetime.fromtimestamp(int(timestamp_str) / 1000)

    def execute_query(self, query, params={}, columns=False):
        """
        Выполняет SQL-запрос к ClickHouse и возвращает результаты.

        :param query: Текст SQL-запроса.
        :return: Результаты запроса.
        """
        result = self.client.query(query, params)
        if columns:
            columns_names = result.column_names
            result_with_columns = []
            for row in result.result_rows:
                result_with_columns.append(dict(zip(columns_names, row)))
            logger.info(f"Executed query: {query} with params: {params}. Columns included.")
            return result_with_columns
        logger.info(f"Executed query: {query} with params: {params}.")
        return result.result_rows
