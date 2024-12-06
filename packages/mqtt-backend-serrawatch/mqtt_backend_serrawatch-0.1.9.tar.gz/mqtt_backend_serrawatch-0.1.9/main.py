import yaml
from SerraWatchLogger.backend.SerraWatchLogger import SerraWatchLogger
from src.mqtt_backend_serrawatch.data.Config import Config
from src.mqtt_backend_serrawatch.MqttClientManager import MQTTClientManager
logger = SerraWatchLogger()

try:
    with open("config.yaml", "r") as file:
        config_dict = yaml.safe_load(file)
        # Créer l'objet Config à partir du dictionnaire
        config = Config.from_dict(config_dict)
        logger.info("Configuration loaded successfully.")

        mqtt_manager = MQTTClientManager(config.broker, config.topics)
        mqtt_manager.connect_and_listen()

except FileNotFoundError:
    logger.error("Configuration file not found.")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
except yaml.YAMLError as e:
    logger.error(f"Error parsing YAML file: {e}")
