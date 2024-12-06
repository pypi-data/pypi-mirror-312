import asyncio
import json
import logging
import time
from collections import defaultdict

import aiohttp

from iqoption_async.expiration import get_expiration_time
from iqoption_async.http.resource import Resource
from iqoption_async.ws.client import WebSocketClient
from iqoption_async.ws.objects.candles import Candles
from iqoption_async.ws.objects.profile import Profile
from iqoption_async.ws.objects.time_sync import TimeSync


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))


class IQOptionAPI:
    profile = Profile()
    timesync = TimeSync()
    candles = Candles()
    order_async = nested_dict(2, dict)
    position_changed = None
    balances_raw: dict = None
    api_option_init_all_result: list = []
    result: dict[str, dict] = {}

    def __init__(self, host: str, username: str, password: str):
        self.https_url = f"https://{host}/api"
        self.wss_url = f"wss://{host}/echo/websocket"
        self.username = username
        self.password = password
        self.session = aiohttp.ClientSession(trust_env=False)
        self.ssl_verify = False
        self.logger = logging.getLogger(__name__)
        self.lock = asyncio.Lock()

    async def close(self):
        await self.websocket_client.websocket.close()

    def set_session(self, cookies: dict, headers: dict):
        self.session.headers.update(headers)
        jar = self.session.cookie_jar
        jar.clear()
        for name, value in cookies.items():
            jar.update_cookies({name: value})

    async def connect(self):
        try:
            await self.close()
        except Exception:
            pass

        check_websocket, websocket_reason = await self.start_websocket()
        if not check_websocket:
            return check_websocket, websocket_reason

        response = await self.get_ssid()
        if isinstance(response, Exception):
            await self.close()
            return False, str(response)

        ssid = response.cookies.get("ssid", None)
        if ssid is None:
            return False, "SSID cookie not found"

        ssid = ssid.value
        await self.send_ssid(ssid)
        self.session.cookie_jar.update_cookies({"ssid": ssid})

        self.timesync.server_timestamp = None
        while self.timesync.server_timestamp is None:
            await asyncio.sleep(0.1)
        return True, None

    async def start_websocket(self):
        self.websocket_client = WebSocketClient(self)
        self.websocket_client_task = asyncio.create_task(self.websocket_client.connect_and_run())

        while True:
            await asyncio.sleep(1)
            if self.websocket_client.websocket_has_error:
                return False, self.websocket_client.websocket_error_reason
            if self.websocket_client.websocket_connected is True:
                return True, None
            if self.websocket_client.websocket_connected is False:
                return False, "Websocket connection closed."

    async def get_ssid(self):
        url = "https://auth.iqoption.com/api/v2/login"
        data = {"identifier": self.username, "password": self.password}
        try:
            return await self.send_http_request_v2(url, "POST", data=data)
        except Exception as e:
            self.logger.error(e)
            return e

    async def send_ssid(self, ssid):
        await self.send_websocket_request("ssid", ssid)
        while self.profile.msg is None:
            await asyncio.sleep(0.1)
        return self.profile.msg is not False

    def prepare_http_url(self, resource: Resource):
        return "/".join((self.https_url, resource.url))

    async def send_http_request(
        self, resource: Resource, method: str, data: dict = None, params: dict = None, headers: dict = None
    ):
        url = self.prepare_http_url(resource)
        self.logger.debug(
            f"{method}: {url} headers {str(self.session.headers)} cookies: {str(self.session.cookie_jar)}"
        )

        async with self.session.request(method=method, url=url, data=data, params=params, headers=headers) as response:
            self.logger.debug(response)
            self.logger.debug(await response.text())
            self.logger.debug(response.headers)
            self.logger.debug(response.cookies)
            response.raise_for_status()
            return response

    async def send_http_request_v2(
        self, url: str, method: str, data: dict = None, params: dict = None, headers: dict = None
    ):
        self.logger.debug(
            f"{method}: {url} headers {str(self.session.headers)} cookies: {str(self.session.cookie_jar)}"
        )

        async with self.session.request(method=method, url=url, data=data, params=params, headers=headers) as response:
            self.logger.debug(response)
            self.logger.debug(await response.text())
            self.logger.debug(response.headers)
            self.logger.debug(response.cookies)
            return response

    def generate_request_id(self):
        return str(int(str(time.time()).split(".")[1]))

    async def send_websocket_request(self, name: str, msg: dict, request_id: str = ""):
        if request_id == "":
            request_id = self.generate_request_id()

        request_id = str(request_id)
        data = json.dumps(dict(name=name, msg=msg, request_id=request_id))
        self.logger.debug(data)

        async with self.lock:
            await self.websocket_client.websocket.send(data)

    async def portfolio(
        self,
        main_name: str,
        name: str,
        instrument_type: str,
        balance_id: int = None,
        user_id: int = None,
        limit: int = 1,
        offset: int = 0,
        request_id: str = "",
    ):
        msg: dict = None
        if name == "portfolio.order-changed":
            msg = {
                "name": name,
                "version": "2.0",
                "params": {"routingFilters": {"instrument_type": instrument_type, "user_id": user_id}},
            }
        elif name == "portfolio.get-positions":
            msg = {
                "name": name,
                "version": "4.0",
                "body": {
                    "instrument_type": instrument_type,
                    "limit": limit,
                    "offset": offset,
                    "user_balance_id": balance_id,
                },
            }
        elif name == "portfolio.position-changed":
            msg = {
                "name": name,
                "version": "3.0",
                "params": {
                    "routingFilters": {
                        "instrument_type": instrument_type,
                        "user_balance_id": balance_id,
                        "user_id": user_id,
                    }
                },
            }

        if msg is None:
            return
        await self.send_websocket_request(main_name, msg, request_id)

    async def set_options(self, request_id: str, send_results):
        msg = {"sendResults": send_results}
        await self.send_websocket_request("setOptions", msg, request_id)

    async def get_balances(self):
        msg = {"name": "get-balances", "version": "1.0"}
        await self.send_websocket_request("sendMessage", msg)

    async def get_api_option_init_all(self):
        msg = {"name": "get-initialization-data", "version": "4.0", "body": {}}
        await self.send_websocket_request("sendMessage", msg)

    async def get_candles(self, active_id: int, interval: int, count: int, end_time: float, request_id: str):
        msg = {
            "name": "get-candles",
            "version": "2.0",
            "body": {
                "active_id": active_id,
                "split_normalization": True,
                "size": interval,
                "count": count,
                "to": int(end_time),
            },
        }
        await self.send_websocket_request("sendMessage", msg, request_id)

    async def buy(self, amount: int, active_id: int, direction: str, expiration: int, request_id: str):
        exp, idx = get_expiration_time(int(self.timesync.server_timestamp), expiration)
        option = None
        if idx < 5:
            option = 3
        else:
            option = 1

        msg = {
            "name": "binary-options.open-option",
            "version": "1.0",
            "body": {
                "price": amount,
                "active_id": active_id,
                "expired": int(exp),
                "direction": direction,
                "option_type_id": option,
                "user_balance_id": int(self.profile.balance_id),
            },
        }
        await self.send_websocket_request("sendMessage", msg, request_id)
