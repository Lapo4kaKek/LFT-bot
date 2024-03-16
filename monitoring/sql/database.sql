CREATE TABLE IF NOT EXISTS orders (
    orderId String,
    exchange String,
    symbol String,
    price Float32,
    qty Float32,
    executedQty Float32,
    totalCost Float32,
    side String,
    orderType String,
    orderStatus String,
    created_time DateTime,
    updated_time DateTime,
    commission Float32
) ENGINE = MergeTree()
ORDER BY (createdTime, order_id);