import yaml
from src.mqtt_backend_serrawatch.data.Config import Config
from src.mqtt_backend_serrawatch.MqttClientManager import MQTTClientManager

from SerraWatchLogger.backend import LoggerSerraWatch
Logger = LoggerSerraWatch.LoggerSerraWatch.get_instance("SerraWatch")

try:
    with open("config.yaml", "r") as file:
        config_dict = yaml.safe_load(file)
        # Créer l'objet Config à partir du dictionnaire
        config = Config.from_dict(config_dict)
        Logger.info(self=Logger, message="Configuration loaded successfully.")

        mqtt_manager = MQTTClientManager(config.broker, config.topics)
        mqtt_manager.connect_and_listen()

except FileNotFoundError:
    Logger.error(self=Logger, message="Configuration file not found.")
except ValueError as e:
    Logger.error(self=Logger, message=f"Configuration error: {e}")
except yaml.YAMLError as e:
    Logger.error(self=Logger, message=f"Error parsing YAML file: {e}")
