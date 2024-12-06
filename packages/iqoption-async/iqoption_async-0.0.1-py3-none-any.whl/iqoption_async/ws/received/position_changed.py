from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqoption_async.api import IQOptionAPI


def position_changed(api: "IQOptionAPI", message: dict):
    name = message.get("name")
    if name != "position-changed":
        return

    msg: dict = message.get("msg", {})
    microservice_name: str = message.get("microserviceName")
    source = msg.get("source")

    if microservice_name == "portfolio":
        if source in ["digital-options", "trading"]:
            order_id = int(msg.get("raw_event")["order_ids"][0])
            api.order_async[order_id][name] = message
            return
        elif source == "binary-options":
            order_id = int(msg.get("external_id"))
            api.order_async[order_id][name] = message
            return

    api.position_changed = message
