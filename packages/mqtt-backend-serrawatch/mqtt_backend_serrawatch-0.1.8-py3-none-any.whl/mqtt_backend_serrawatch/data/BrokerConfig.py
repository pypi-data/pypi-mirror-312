from ..utils import CustomLogger

Logger = CustomLogger()
class BrokerConfig:
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port
        Logger.debug(f"BrokerConfig initialized with address: {address}, port: {port}")