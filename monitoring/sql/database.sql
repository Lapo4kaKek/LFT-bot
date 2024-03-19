CREATE TABLE IF NOT EXISTS orders (
    orderId String,
    exchange String,
    symbol String,
    price Decimal(38, 20),
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
    strategyId String,
    name String,
    exchange String,
    symbol String,
    balance Decimal(38, 20),
    activeTokens Decimal(38, 20),
    assetsNumber Decimal(38, 20),
    status Boolean,
    createdTime DateTime
) ENGINE = MergeTree()
ORDER BY (createdTime);