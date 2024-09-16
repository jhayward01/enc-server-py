import os
import yaml


class ConfigFile:
    @staticmethod
    def verify_configs(configs: dict, expected: list) -> (bool, str):
        for field in expected:
            if field not in configs.keys():
                return False, field
        return True, ''

    @staticmethod
    def load_configs(config_path: str) -> dict:
        val = os.getenv("ENC_SERVER_GO_CONFIG_PATH")
        if val:
            config_path = val

        with open(config_path, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
