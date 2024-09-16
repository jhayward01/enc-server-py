import logging

from enc_server import be
from enc_server import utils

module_name = "beserver"
config_name = "beServerConfigs"
config_path = "config/config.yaml"

if __name__ == '__main__':
    utils.start_logger(module_name)
    logging.info(f"Started {module_name}")

    configs = utils.ConfigFile.load_configs(config_path)
    server = be.server.Server(configs[config_name])

    server.start()
