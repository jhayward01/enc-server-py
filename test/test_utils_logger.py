import logging
import unittest

import enc_server


class LoggerTestSuite(unittest.TestCase):
    expected_lines = 4

    def test_start_logger(self):
        log_path = enc_server.utils.Logger.start_logger("beclient")

        logging.debug("Debug message")
        logging.info("Info message")
        logging.warning("Warning message")
        logging.error("Error message")

        with open(log_path, 'r') as fp:
            lines = len(fp.readlines())
            self.assertEqual(LoggerTestSuite.expected_lines, lines)
