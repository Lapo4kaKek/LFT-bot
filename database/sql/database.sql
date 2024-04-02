CREATE TABLE IF NOT EXISTS orders (
    orderId String,
    exchange String,
    symbol String,
    price Decimal(38, 20),
    stopPrice Decimal(38, 20),
    qty Decimal(38, 20),
    executedQty Decimal(38, 20),
    totalCost Decimal(38, 20),
    side String,
    orderType String,
    orderStatus String,
    createdTime DateTime,
    updatedTime DateTime,
    commission Decimal(38, 20)
) ENGINE = MergeTree()
ORDER BY (createdTime, orderId);


CREATE TABLE IF NOT EXISTS strategies (
    strategyId UUID DEFAULT generateUUIDv4(),
    name String,
    type String,
    exchange String,
    symbol String,
    balance Decimal(38, 20),
    assetsNumber Decimal(38, 20),
    status Boolean,
    createdTime DateTime
) ENGINE = MergeTree()
ORDER BY (createdTime);

CREATE TABLE order_strategy_link
(
    orderId String,
    strategyId String
) ENGINE = MergeTree()
ORDER BY (order_id, strategy_id);
