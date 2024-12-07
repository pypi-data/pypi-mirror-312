import paho.mqtt.client as mqtt
from .data import TopicsConfig, BrokerConfig

from SerraWatchLogger.backend import LoggerSerraWatch
Logger = LoggerSerraWatch.LoggerSerraWatch.get_instance("SerraWatch")

class MQTTClientManager:
    def __init__(self, broker_config: BrokerConfig, topics_config: TopicsConfig):
        self.broker_config = broker_config
        self.topics_config = topics_config
        self.client = mqtt.Client()

        # Assign callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        Logger.debug(self=Logger, message="MQTTClientManager initialized.")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            Logger.info(self=Logger, message="Connected to MQTT Broker successfully.")
            # Souscrire à plusieurs topics
            self.client.subscribe([
                (self.topics_config.publisher, 0),
                (self.topics_config.subscriber, 1)
            ])
        else:
            Logger.error(self=Logger, message=f"Failed to connect to MQTT Broker. Return code: {rc}")

    def on_message(self, client, userdata, msg):
        Logger.info(self=Logger, message=f"Message received: Topic: {msg.topic}, Payload: {msg.payload.decode()}")
        Logger.add_topic_log(self=Logger,  topics=msg.topic, messages=f"Message received: Topic: {msg.topic}, Payload: {msg.payload.decode()}")

    def connect_and_listen(self):
        try:
            Logger.debug(self=Logger, message=f"Connecting to broker at {self.broker_config.address}:{self.broker_config.port}")
            self.client.connect(self.broker_config.address, self.broker_config.port, 60)
            # Start listening (blocking loop)
            self.client.loop_forever()
        except Exception as e:
            Logger.error(self=Logger, message=f"Error while connecting to MQTT broker: {e}")

    def disconnect_and_stop(self):
        try:
            Logger.debug(self=Logger, message="Disconnecting from MQTT Broker and stopping the loop.")
            self.client.disconnect()  # Déconnecte le client du broker
            self.client.loop_stop()  # Arrête la boucle d'écoute
            Logger.info(self=Logger, message="Disconnected from MQTT Broker successfully.")
        except Exception as e:
            Logger.error(self=Logger, message=f"Error while disconnecting from MQTT broker: {e}")