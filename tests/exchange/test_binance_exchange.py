import pytest
from unittest.mock import patch, MagicMock
from exchange.binance_exchange import BinanceExchange
from monitoring.monitoring import Monitoring


@pytest.fixture
def binance():
    monitoring_mock = MagicMock(spec=Monitoring)
    return BinanceExchange('api_key', 'api_secret', monitoring_mock)


@patch('exchange.binance_exchange.ccxt.binance')
def test_create_market_buy_order(binance_mock, binance):
    binance_mock.return_value.create_order.return_value = {
        'info': {
            'orderId': '123',
            'symbol': 'BTC/USDT',
            'executedQty': '1',
            'cummulativeQuoteQty': '10000',
            'fills': [{'price': '10000', 'qty': '1', 'commission': '10', 'commissionAsset': 'USDT'}],
            'status': 'closed',
            'type': 'market',
            'side': 'buy',
            'workingTime': '1617000000'
        },
        'id': '123',
        'timestamp': 1617000000000,
        'datetime': '2021-03-29 12:00:00',
        'symbol': 'BTC/USDT',
        'type': 'market',
        'side': 'buy',
        'price': 10000,
        'amount': 1
    }

    result = binance.create_market_buy_order('BTC/USDT', 1)

    assert result['symbol'] == 'BTC/USDT'
    assert result['type'] == 'market'
    assert result['side'] == 'buy'
    assert result['price'] == 10000
    assert result['amount'] == 1

    binance.monitoring.insert_single_order_to_db.assert_called_once()
