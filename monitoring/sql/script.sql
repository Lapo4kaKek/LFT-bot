CREATE TABLE orders (
    order_id String,
    symbol String,
    price Float64,
    qty Float64,
    side String,
    order_type String,
    order_status String,
    created_time DateTime,
    updated_time DateTime
) ENGINE = MergeTree() ORDER BY (created_time, order_id);


INSERT INTO orders (order_id, symbol, price, qty, side, order_type, order_status, created_time, updated_time) VALUES ('419eb2eb-32d1-4934-8bac-b88aaa6248fb', 'STRKUSDT', 2.323, 2, 'Sell', 'Market', 'Filled', '2024-03-13 00:00:00', '2024-03-13 00:00:03');