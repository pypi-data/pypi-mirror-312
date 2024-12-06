import logging
from cli_logger.logger import LoggerConfig

logger_config = {
    LoggerConfig.MAIN_LEVEL: logging.DEBUG,
    LoggerConfig.CONSOLE_LEVEL: logging.DEBUG,
    LoggerConfig.FILE_LEVEL: logging.DEBUG
}
