import time
from datetime import datetime, timedelta


class TimeSync:
    def __init__(self) -> None:
        self.name = "timeSync"
        self.server_timestamp = None
        self.expiration_time = 1

    @property
    def server_datetime(self):
        while self.server_timestamp is None:
            time.sleep(0.2)
        return datetime.fromtimestamp(self.server_timestamp)

    @property
    def expiration_datetime(self):
        return self.server_datetime + timedelta(minutes=self.expiration_time)

    @property
    def expiration_timestamp(self):
        return time.mktime(self.expiration_datetime.timetuple())
