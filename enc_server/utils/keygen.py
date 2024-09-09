import config


class Keygen:

    def __init__(self, configs):
        result, missing = config.verify_configs(configs, ["keySize"])
        if not result:
            raise KeyError("Keygen missing configuration " + missing)

        self.key_size = int(configs["keySize"])
