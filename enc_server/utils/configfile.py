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
        config_path = os.environ.get('ENC_SERVER_GO_CONFIG_PATH', config_path)

        with open(config_path, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
