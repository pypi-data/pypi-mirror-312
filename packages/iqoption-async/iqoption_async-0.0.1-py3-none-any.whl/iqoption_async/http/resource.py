from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqoption_async.api import IQOptionAPI


class Resource:
    url = ""

    def __init__(self, api: "IQOptionAPI"):
        self.api = api

    async def send_http_request(self, method: str, data: dict = None, params: dict = None, headers: dict = None):
        return await self.api.send_http_request(self, method, data, params, headers)
