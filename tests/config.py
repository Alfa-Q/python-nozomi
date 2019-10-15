""" Configuration for tests."""

import logging


_LOGFILE_NAME = 'test_output.log'


def setup_logger():
    """Setup the logger for testing.
    """
    logging.basicConfig(
        filename=_LOGFILE_NAME,
        filemode='w',
        level=logging.DEBUG,
        format='%(levelname)-8s Module: %(name)-15s Function: %(funcName)-20s: %(message)s'
    )
