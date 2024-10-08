import logging
import time
import traceback

import enc_server

module_name = "beclient"
config_name = "beClientConfigs"
params_name = "testParams"
config_path = "config/config.yaml"

if __name__ == '__main__':
    try:
        enc_server.utils.Logger.start_logger(module_name)
        logging.info(f"Started {module_name}")

        configs = enc_server.utils.ConfigFile.load_configs(config_path)
        logging.info(configs[config_name])

        client = enc_server.be.client.Client(configs[config_name])

        record_id = configs[params_name]["id"]
        record_payload = configs[params_name]["record"]

        logging.info(f"Storing record {record_id} {record_payload}")
        result = client.store(record_id, record_payload)
        logging.info(f"Store received {result}")
        time.sleep(2)

        logging.info(f"Retrieving record {record_id}")
        result = client.retrieve(record_id)
        logging.info(f"Retrieve received {record_id} {result}")
        time.sleep(2)

        logging.info(f"Deleting record {record_id}")
        result = client.delete(record_id)
        logging.info(f"Delete received {result}")
        time.sleep(2)

    except Exception as err:
        logging.fatal(err)
        logging.fatal(traceback.format_exc())
