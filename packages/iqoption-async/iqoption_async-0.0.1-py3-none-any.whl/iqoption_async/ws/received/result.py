from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqoption_async.api import IQOptionAPI


def result(api: "IQOptionAPI", message: dict):
    if message.get("name") == "result":
        request_id = message.get("request_id")
        if request_id in api.result:
            api.result[request_id]["result"] = message.get("msg", {"success": None})["success"]
