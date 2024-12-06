from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqoption_async.api import IQOptionAPI


def candles(api: "IQOptionAPI", message: dict):
    if message.get("name") == "candles":
        request_id = message.get("request_id")
        if api.candles.has_request_id(request_id):
            api.candles.set_candles_data(request_id, message.get("msg")["candles"])
