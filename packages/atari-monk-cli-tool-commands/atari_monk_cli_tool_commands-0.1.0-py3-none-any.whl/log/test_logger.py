from cli_logger.logger import setup_logger
from log_task.log_setup import getConsoleFileLoggerConfig

def log_test_command(_):
    custom_config = getConsoleFileLoggerConfig(__name__)

    logger = setup_logger(__name__, custom_config)

    logger.info(f'__name__: {__name__}')
    logger.info(f'custom_config: {custom_config}')

    logger.debug("This is a debug message.")
    logger.info("This is an informational message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical error message.")

    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.exception("An exception occurred: %s", e)
