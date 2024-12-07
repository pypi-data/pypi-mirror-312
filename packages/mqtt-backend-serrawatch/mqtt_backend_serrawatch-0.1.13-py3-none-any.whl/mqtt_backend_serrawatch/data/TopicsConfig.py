
from SerraWatchLogger.backend import LoggerSerraWatch
Logger = LoggerSerraWatch.LoggerSerraWatch.get_instance("SerraWatch")

class TopicsConfig:
    def __init__(self, publisher: str, subscriber: str):
        self.publisher = publisher
        self.subscriber = subscriber
        Logger.debug(self=Logger, message=f"TopicsConfig initialized with publisher: {publisher}, subscriber: {subscriber}")