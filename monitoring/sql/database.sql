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
    createdTime DateTime,
    updatedTime DateTime,
    commission Float32
) ENGINE = MergeTree()
ORDER BY (createdTime, orderId);