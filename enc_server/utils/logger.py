import datetime
import logging
import os


class Logger:
    default_dir = "/tmp/enc-server-go-logs"
    env_var = "ENC_SERVER_PY_LOG_DIR"

    @staticmethod
    def start_logger(name: str) -> str:
        log_dir = os.environ.get(Logger.env_var, Logger.default_dir)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        log_name = name + "." + timestamp + ".log"
        log_path = os.path.join(log_dir, log_name)

        log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

        if os.environ.get(Logger.env_var, "true").lower() == "true":
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(log_formatter)
            root_logger.addHandler(console_handler)

        return log_path
