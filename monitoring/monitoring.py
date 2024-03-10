import clickhouse_connect


class Monitoring:
    def __init__(self, host='localhost', port=8123, username='default', password=''):
        self.client = clickhouse_connect.get_client(host=host, port=port, username=username, password=password)

    def create_table(self, table_name, columns):
        columns_with_types = ', '.join([f'{name} {type}' for name, type in columns.items()])
        create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types}) ENGINE = MergeTree() ORDER BY tuple()'
        self.client.command(create_table_query)

    def insert_data(self, table_name, data, column_names=None):
        self.client.insert(table_name, data, column_names=column_names)

    def fetch_and_print_table_data(self, table_name):
        result = self.client.query(f'SELECT * FROM {table_name}')
        for row in result.result_rows:
            print(row)


