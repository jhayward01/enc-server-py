import logging
import os
import yaml


class ConfigFile:
    env_var = "ENC_SERVER_PY_CONFIG_PATH"

    @staticmethod
    def verify_configs(configs: dict, expected: list) -> (bool, str):
        for field in expected:
            if field not in configs.keys():
                return False, field
        return True, ''

    @staticmethod
    def load_configs(config_path: str) -> dict:
        config_path = os.environ.get(ConfigFile.env_var, config_path)
        logging.info(f"Loading config file '{config_path}'")

        with open(config_path, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
