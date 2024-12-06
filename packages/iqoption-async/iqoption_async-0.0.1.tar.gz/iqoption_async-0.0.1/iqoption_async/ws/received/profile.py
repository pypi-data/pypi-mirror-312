from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqoption_async.api import IQOptionAPI


def profile(api: "IQOptionAPI", message: dict):
    if message.get("name") != "profile":
        return

    api.profile.msg = message.get("msg")
    if api.profile.msg is None or api.profile.msg is False:
        return

    msg: dict = message.get("msg", {})

    api.profile.id = msg.get("user_id")
    api.profile.balance_id = msg.get("balance_id")
    api.profile.balance_type = msg.get("balance_type")
    api.profile.balances = msg.get("balances")
