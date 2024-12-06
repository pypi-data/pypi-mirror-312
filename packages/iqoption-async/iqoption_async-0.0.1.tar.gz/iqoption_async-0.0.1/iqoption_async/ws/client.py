import json
import logging
import ssl

from websockets.asyncio.client import connect

from iqoption_async.ws.received.balances import balances
from iqoption_async.ws.received.candles import candles
from iqoption_async.ws.received.initialization_data import initialization_data
from iqoption_async.ws.received.option import option
from iqoption_async.ws.received.position_changed import position_changed
from iqoption_async.ws.received.profile import profile
from iqoption_async.ws.received.result import result
from iqoption_async.ws.received.time_sync import time_sync


class WebSocketClient:
    def __init__(self, api) -> None:
        self.api = api
        self.uri = self.api.wss_url
        self.logger = logging.getLogger(__name__)
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.websocket = None
        self.websocket_error_reason = None
        self.websocket_has_error = False
        self.websocket_connected = None
        self.user_agent_header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"  # noqa: E501

    async def check_is_connected(self):
        try:
            await self.websocket.ping()
            return True
        except Exception:
            return False

    async def connect_and_run(self):
        try:
            async with connect(
                self.uri, ssl=self.ssl_context, max_size=None, user_agent_header=self.user_agent_header
            ) as websocket:
                self.websocket = websocket
                self.logger.debug("Websocket client connected.")
                self.websocket_connected = True
                await self.receive()
        except Exception as e:
            self.logger.debug(f"Websocket error {e}")
            self.websocket_error_reason = str(e)
            self.websocket_has_error = True
        finally:
            self.logger.debug("Websocket connection closed.")
            self.websocket_connected = False

    async def receive(self):
        try:
            async for message in self.websocket:
                await self.on_message(message)
        except Exception as e:
            self.logger.error(f"Error during receiving messages: {e}")
            self.websocket_error_reason = str(e)
            self.websocket_has_error = True

    async def on_message(self, message):
        message = json.loads(str(message))

        result(self.api, message)
        candles(self.api, message)
        profile(self.api, message)
        time_sync(self.api, message)
        position_changed(self.api, message)
        balances(self.api, message)
        initialization_data(self.api, message)
        option(self.api, message)
