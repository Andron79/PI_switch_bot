import logging
from logging.handlers import SysLogHandler

from tolik_bot import settings


def get_logger(key: str = 'tolik_bot'):
    logger = logging.getLogger(key)
    if logger.handlers:
        return logger

    level = logging.DEBUG if settings.DEBUG else logging.INFO
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    handler_console = logging.StreamHandler()
    handler_console.setLevel(level)
    handler_console.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler_console)

    try:
        handler_syslog = SysLogHandler()
    except OSError:
        logger.error("Failed to setup syslog handler")
    else:
        handler_syslog.setLevel(level)
        handler_syslog.setFormatter(formatter)
        logger.addHandler(handler_syslog)

    return logger
