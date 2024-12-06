from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqoption_async.api import IQOptionAPI


def balances(api: "IQOptionAPI", message: dict):
    if message.get("name") == "balances":
        api.balances_raw = message
