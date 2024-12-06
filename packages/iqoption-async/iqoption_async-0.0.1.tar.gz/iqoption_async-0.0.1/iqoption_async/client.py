import asyncio
import logging
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta
from random import randint

import pytz

from iqoption_async.api import IQOptionAPI
from iqoption_async.constants import ACTIVES
from iqoption_async.version_control import API_VERSION


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))


class IQOptionClient:
    __version__ = API_VERSION
    api: IQOptionAPI

    OPEN_TIME = nested_dict(3, dict)
    PROFITS = nested_dict(3, dict)

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.logger = logging.getLogger(__name__)

        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"  # noqa: E501
        self.session_header = {"User-Agent": agent}
        self.session_cookie = {}

    async def close(self):
        await self.api.close()

    async def connect(self):
        self.api = IQOptionAPI("iqoption.com", self.email, self.password)
        self.api.set_session(self.session_cookie, self.session_header)

        check, reason = await self.api.connect()
        if not check:
            return False, reason

        while self.api.profile.balance_id is None:
            await asyncio.sleep(0.1)

        tasks = []
        tasks.append(self.position_change_all("subscribeMessage", self.api.profile.balance_id))
        tasks.append(self.order_changed_all("subscribeMessage"))
        tasks.append(self.api.set_options(1, True))
        tasks.append(self.get_all_open_time())
        await asyncio.gather(*tasks)
        return True, None

    async def position_change_all(self, main_name: str, balance_id: str):
        instrument_type = ["cfd", "forex", "crypto", "digital-option", "turbo-option", "binary-option"]
        tasks = []
        for ins in instrument_type:
            tasks.append(
                self.api.portfolio(main_name, "portfolio.position-changed", ins, balance_id, self.api.profile.id)
            )
        await asyncio.gather(*tasks)

    async def order_changed_all(self, main_name: str):
        instrument_type = [
            "cfd",
            "forex",
            "crypto",
            "digital-option",
            "turbo-option",
            "binary-option",
            "turbo",
            "binary",
        ]
        tasks = []
        for ins in instrument_type:
            tasks.append(self.api.portfolio(main_name, "portfolio.order-changed", ins, user_id=self.api.profile.id))
        await asyncio.gather(*tasks)

    async def check_connect(self):
        return await self.api.websocket_client.check_is_connected()

    async def get_profile(self):
        while self.api.profile.msg is None:
            await asyncio.sleep(0.1)
        return self.api.profile

    async def change_balance(self, balance_mode: str):
        real_id = None
        practice_id = None
        tournament_id = None

        profile = await self.get_profile()
        for balance in profile.balances:
            balance_type = balance.get("type")
            balance_id = balance.get("id")
            if balance_type == 1:
                real_id = balance_id
            if balance_type == 4:
                practice_id = balance_id
            if balance_type == 2:
                tournament_id = balance_id

        if balance_mode == "REAL":
            await self.__set_balance_mode(real_id)
        elif balance_mode == "PRACTICE":
            await self.__set_balance_mode(practice_id)
        elif balance_mode == "TOURNAMENT":
            await self.__set_balance_mode(tournament_id)
        else:
            self.logger.error(f"ERROR {balance_mode} does not exists")
            await self.close()
            sys.exit(1)

    async def __set_balance_mode(self, balance_id: int):
        if self.api.profile.balance_id == balance_id:
            return
        if self.api.profile.balance_id is not None:
            await self.position_change_all("unsubscribeMessage", self.api.profile.balance_id)
        self.api.profile.balance_id = balance_id
        await self.position_change_all("subscribeMessage", balance_id)

    async def get_balance(self):
        if self.api.profile.balance_id is None:
            self.logger.error("ERROR balance account not configured")
            return None
        balances_raw = await self.get_balances()
        for balance in balances_raw.get("msg"):
            if balance["id"] == self.api.profile.balance_id:
                return balance["amount"]
        return None

    async def get_balances(self):
        self.api.balances_raw = None
        await self.api.get_balances()
        while self.api.balances_raw is None:
            await asyncio.sleep(0.1)
        return self.api.balances_raw

    async def get_all_open_time(self):
        self.OPEN_TIME = nested_dict(3, dict)
        tasks = [self.__get_binary_open()]
        await asyncio.gather(*tasks)
        return self.OPEN_TIME

    async def get_all_init(self):
        self.api.api_option_init_all_result = None
        if not (await self.check_connect()):
            await self.connect()

        await self.api.get_api_option_init_all()
        start_at = time.time()
        retries = 0
        max_retries = 3
        while True:
            while self.api.api_option_init_all_result is None:
                if time.time() - start_at >= 30:
                    self.logger.error("WARN get_api_option_init_all late 30 sec")
                    break
                await asyncio.sleep(0.1)
            if self.api.api_option_init_all_result is not None:
                break
            retries += 1
            if retries >= max_retries:
                return None
            await asyncio.sleep(0.1)

        return self.api.api_option_init_all_result

    async def __get_binary_open(self):
        binary_data = await self.get_all_init()
        binary_list = ["binary", "turbo"]
        if binary_data is None:
            return
        for option in binary_list:
            if option not in binary_data:
                continue

            actives: dict[int, dict] = binary_data[option]["actives"]
            for i, details in actives.items():
                name_part = str(details["name"].split(".")[1])
                ACTIVES[name_part] = int(i)

                is_open = details.get("enabled", False) and not details.get("is_suspended", True)
                self.OPEN_TIME[option][name_part]["open"] = is_open
                self.OPEN_TIME[option][name_part]["schedules"] = details.get("schedule", [])

                option_profit = details.get("option", {"profit": {"commission": 100}})["profit"]
                commission = option_profit["commission"]
                profit = (100.0 - commission) / 100.0
                self.PROFITS[option][name_part]["profit"] = profit

    async def __check_order(self, order_id: int, expiration: int):
        expiration = datetime.now(pytz.utc) + timedelta(minutes=expiration, seconds=10)
        while True:
            now = datetime.now(pytz.utc)
            if now >= expiration:
                self.logger.warning(f"ERROR order not found after {expiration} mins")
                return False, None, None

            order = self.api.order_async.get(order_id)
            if order is None:
                await asyncio.sleep(0.1)
                continue
            detail: dict = order.get("position-changed", {}).get("msg")
            if detail is None:
                await asyncio.sleep(0.1)
                continue
            status = detail.get("status")
            close_reason = detail.get("close_reason")
            pnl = detail.get("pnl")
            if status != "closed" or close_reason is None or pnl is None:
                await asyncio.sleep(0.1)
                continue
            return True, close_reason, pnl

    async def check_order(self, order_id: int, expiration: int = 1, async_fnc=None):
        order_id = int(order_id)

        async def call_fnc(_fnc, _order_id: int, _expiration: int):
            result = await self.__check_order(_order_id, _expiration)
            await _fnc(result)

        if async_fnc is not None:
            asyncio.create_task(call_fnc(async_fnc, order_id, expiration))
            return

        return await self.__check_order(order_id, expiration)

    async def get_candles(self, symbol: str, interval_min: int, limit: int, end_time: float):
        if symbol not in ACTIVES:
            self.logger.warning(f"Asset {symbol} not found")
            return None

        request_id = self.api.generate_request_id()
        self.api.candles.add_request_id(request_id)
        interval_min *= 60
        await self.api.get_candles(ACTIVES[symbol], interval_min, limit, end_time, request_id)
        candles_data = self.api.candles.get_candles_data(request_id)
        while candles_data is None:
            await asyncio.sleep(0.1)
            candles_data = self.api.candles.get_candles_data(request_id)
            if not (await self.check_connect()):
                self.logger.error("ERROR get_candles need reconnect")
                break
        return candles_data

    async def get_profit(self, symbol: str, option_type: str):
        par = self.PROFITS.get(option_type, {}).get(symbol)
        if par is None:
            return None
        return par["profit"]

    async def buy(self, amount: float, symbol: str, action: str, expiration: int):
        if self.api.profile.balance_id is None:
            self.logger.error("ERROR balance account not configured")
            return False, None
        if symbol not in ACTIVES:
            self.logger.warning(f"Asset {symbol} not found")
            return False, None
        request_id = str(randint(0, 10000))
        active_id = ACTIVES[symbol]
        action = action.lower()
        self.api.result[request_id] = {"result": None, "id": None}

        await self.api.buy(float(amount), active_id, action, expiration, request_id)
        start_at = datetime.now(pytz.utc) + timedelta(seconds=5)
        order_id = None
        order_result = None
        while True:
            now = datetime.now(pytz.utc)
            if now >= start_at:
                self.logger.error("WARNINING buy late 5 sec")
                print(self.api.result)
                return False, None, None

            order = self.api.result[request_id]
            message = order.get("message")
            if message is not None:
                self.api.result.pop(request_id)
                return False, message, None

            order_id = order.get("id")
            order_expiration = order.get("exp")
            order_result = order.get("result")
            if order_id is not None and order_result is not None:
                self.api.result.pop(request_id)
                return order_result, order_id, order_expiration
            await asyncio.sleep(0.1)
