from SerraWatchLogger.backend.LoggerSerraWatch import LoggerSerraWatch

Logger = LoggerSerraWatch.get_instance("SerraWatch")
class BrokerConfig:
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port
        Logger.debug(f"BrokerConfig initialized with address: {address}, port: {port}")