import time

import allure
import cerberus
import pytest

from connectors.binance_futures import BinanceFuturesClient
from keys import Futures_Secret_Key, Futures_API_Key
from tests.tests_api.schemas import schema_price_info


@allure.feature("API Tests")
class Test_Api:
    @allure.title("Test that response is validates with schema")
    @pytest.mark.parametrize("value", ["BTCUSDT", "PEOPLEUSDT", "ETHUSDT"])
    def test_validate_response_with_schema(self, value):
        binance = BinanceFuturesClient(Futures_API_Key, Futures_Secret_Key)
        response = binance.get_symbol_price_ticker(params={'symbol': value})
        v = cerberus.Validator()
        assert v.validate(response, schema_price_info)

    @allure.title("Test that connection is established")
    def test_connectivity(self):
        binance = BinanceFuturesClient(Futures_API_Key, Futures_Secret_Key)
        connection_status = binance.test_connectivity()
        assert connection_status == {}

    @allure.title("Test that time on PC and on Server differs by no more than 1 second")
    def test_server_time(self):
        binance = BinanceFuturesClient(Futures_API_Key, Futures_Secret_Key)
        server_time = binance.check_server_time()
        assert abs(int(*server_time.values()) - round(time.time() * 1000)) < 1000

    def test_get_current_balance(self):
        binance = BinanceFuturesClient(Futures_API_Key, Futures_Secret_Key)
        b = binance.get_balance()
        assert round(float(b['totalWalletBalance']), 2) == 14982.40

    # Todo: переделать
    # def test_get_all_current_open_orders(self):
    #     binance = BinanceFuturesClient(Futures_API_Key, Futures_Secret_Key)
    #     b = binance.get_all_current_open_orders()
    #     print(b)

    # def test_place_order(self, base_url):
    #     payload = {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'BUY', 'timestamp': timestamp, 'quantity': round(0.001, 8), 'order_type': 'MARKET', 'signature': self._generate_signature()}
    #     # binance = BinanceFuturesClient(Futures_API_Key, Futures_Secret_Key)
    #     r = requests.post("https://testnet.binancefuture.com/fapi/v1/order", data=payload)
    #     print(r.json())
