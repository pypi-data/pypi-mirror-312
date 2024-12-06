from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqoption_async.api import IQOptionAPI


def initialization_data(api: "IQOptionAPI", message: dict):
    if message.get("name") == "initialization-data":
        api.api_option_init_all_result = message.get("msg")
