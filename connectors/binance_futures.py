import hashlib
import hmac
import time
import typing
from urllib.parse import urlencode

import requests


class BinanceFuturesClient:
    """https://binance-docs.github.io/apidocs/futures/en/#change-log"""

    def __init__(self, public_key: str, secret_key: str):
        self._base_url = "https://testnet.binancefuture.com"
        self._public_key = public_key
        self._secret_key = secret_key
        self._headers = {'X-MBX-APIKEY': self._public_key}

    def test_connectivity(self):
        return self._make_request("GET", "/fapi/v1/ping", dict())

    def check_server_time(self):
        return self._make_request("GET", "/fapi/v1/time", dict())

    def get_symbol_price_ticker(self, params):
        return self._make_request("GET", "/fapi/v1/ticker/price", params)

    def _generate_signature(self, data: typing.Dict) -> str:
        return hmac.new(self._secret_key.encode("utf-8"), urlencode(data).encode("utf-8"), hashlib.sha256).hexdigest()

    def _make_request(self, method: str, endpoint: str, data: typing.Dict):
        if method == 'GET':
            try:
                response = requests.get(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                return ValueError

        elif method == "POST":
            try:
                response = requests.post(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                return ValueError(f"Connection error while making {method} request to {endpoint}: {e}")

        elif method == "DELETE":
            try:
                response = requests.delete(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                return ValueError(f"Connection error while making {method} request to {endpoint}: {e}")

        else:
            raise ValueError("ERROR with request")

        if response.status_code == 200:
            return response.json()
        else:
            return ValueError("Error while making %s request to %s: %s (error code %s)", method, endpoint,
                              response.json(), response.status_code)

    def get_balance(self):
        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self._generate_signature(data)
        return self._make_request("GET", "/fapi/v2/account", data)

    # #todo: поправить
    # def get_all_current_open_orders(self):
    #     data = dict()
    #     data['timestamp'] = int(time.time() * 1000)
    #     data['signature'] = self._generate_signature(data)
    #     orders = []
    #     current_open_orders = self._make_request("GET", "/fapi/v1/openOrders", data)
    #
    #     return orders

    # def get_exchange_info(self):
    #     return self._make_request("GET", "/fapi/v1/exchangeInfo", dict())
