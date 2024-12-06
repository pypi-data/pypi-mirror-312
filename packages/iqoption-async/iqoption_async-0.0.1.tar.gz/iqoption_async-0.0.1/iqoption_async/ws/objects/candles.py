class Candles:
    def __init__(self):
        self.name = "candles"
        self.__candles_data = {}

    def get_candles_data(self, request_id: str):
        if self.__candles_data.get(request_id) is None:
            return None
        return self.__candles_data.pop(request_id, None)

    def set_candles_data(self, request_id: str, candles_data):
        self.__candles_data[request_id] = candles_data

    def add_request_id(self, request_id: str):
        if not self.has_request_id(request_id):
            self.__candles_data[request_id] = None

    def has_request_id(self, request_id: str):
        return request_id in self.__candles_data
