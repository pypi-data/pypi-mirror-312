import unittest
import arklog


class LogTest(unittest.TestCase):
    """"""

    def setUp(self):
        """Set up test fixtures, if any."""
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_simple_log(self):
        logger = arklog.create_logger("Test-Logger", arklog.DEBUG)
        logger.debug("Debug message")
        logger.extra("Extra")
        logger.success("Completed")

        arklog.set_defaults()
        arklog.debug("Debug message")
        arklog.info("Debug message")
        arklog.warning("Debug message")
        arklog.extra("Extra")
        arklog.success("Completed")

    def test_dict_log(self):
        arklog.set_config_logging()
        arklog.debug("Debug message")
        arklog.info("Debug message")
        arklog.warning("Debug message")
        arklog.extra("Extra")
        arklog.success("Completed")
