from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqoption_async.api import IQOptionAPI


def option(api: "IQOptionAPI", message: dict):
    if message.get("name") == "option":
        request_id = message.get("request_id")
        if request_id in api.result:
            msg: dict = message.get("msg", {})
            for key, val in msg.items():
                if key in ["id", "message", "exp"]:
                    api.result[request_id][key] = val
