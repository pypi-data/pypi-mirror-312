from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqoption_async.api import IQOptionAPI


def time_sync(api: "IQOptionAPI", message: dict):
    if message.get("name") == "timeSync":
        server_timestamp = message.get("msg")
        if server_timestamp is not None:
            api.timesync.server_timestamp = server_timestamp / 1000
