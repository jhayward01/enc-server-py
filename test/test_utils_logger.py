import enc_server
import logging
import unittest


class LoggerTestSuite(unittest.TestCase):
    expected_lines = 4

    def test_start_logger(self):
        log_path = enc_server.utils.start_logger("beclient")

        logging.debug("Debug message")
        logging.info("Info message")
        logging.warning("Warning message")
        logging.error("Error message")

        with open(log_path, 'r') as fp:
            lines = len(fp.readlines())
            self.assertEqual(LoggerTestSuite.expected_lines, lines)
