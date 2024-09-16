import logging

import enc_server

module_name = "beserver"
config_name = "beServerConfigs"
config_path = "config/config.yaml"

if __name__ == '__main__':
    try:
        enc_server.utils.Logger.start_logger(module_name)
        logging.info(f"Started {module_name}")

        configs = enc_server.utils.ConfigFile.load_configs(config_path)
        server = enc_server.be.server.Server(configs[config_name])

        server.start()
    except Exception as err:
        logging.fatal(err)
