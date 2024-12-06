import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqoption_async.api import IQOptionAPI


class Base:
    def __init__(self, api: "IQOptionAPI"):
        self.api = api

    def send_websocket_request(self, name: str, msg: dict, request_id: str = ""):
        if request_id == "":
            request_id = str(int(str(time.time()).split(".")[1]))
        return self.api.send_websocket_request(name, msg, request_id)
