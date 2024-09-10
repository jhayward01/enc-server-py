import os
import datetime
import logging
from io import TextIOWrapper

default_dir = "/tmp/enc-server-go-logs"


def start_logger(name: str) -> str:
    log_dir = os.environ.get('ENC_SERVER_GO_LOG_DIR', default_dir)

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

    if os.environ.get('ENC_SERVER_GO_LOG_STDOUT', "true").lower() == "true":
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)

    return log_path
