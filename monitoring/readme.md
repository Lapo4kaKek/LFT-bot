### You need install:
```python
pip3 install clickhouse-driver
```

### Пример использования
```python
monitoring = Monitoring('localhost', 8123, "admin", "admin")
monitoring.create_table('example_table', {'id': 'Int32', 'name': 'String'})

data = [
    (1, 'Alice'),
    (2, 'Bob'),
    (3, 'Charlie')
]
monitoring.insert_data('example_table', data)

monitoring.fetch_and_print_table_data("example_table")
```

