import logging

import enc_server

module_name = "feserver"
config_name = "feServerConfigs"
client_name = "beClientConfigs"
config_path = "config/config.yaml"

if __name__ == '__main__':
    try:
        enc_server.utils.Logger.start_logger(module_name)
        logging.info(f"Started {module_name}")

        configs = enc_server.utils.ConfigFile.load_configs(config_path)
        logging.info(configs)

        server = enc_server.fe.server.Server(dict(configs[config_name], **configs[client_name]))

        server.start(server_config=True)
    except Exception as err:
        logging.fatal(err)
