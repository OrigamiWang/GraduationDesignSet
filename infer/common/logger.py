import logging
import traceback

LOGGER = None

class CustomFormatter(logging.Formatter):

    reset = "\x1b[0m"
    red = "\x1b[31;20m"
    green = "\x1B[32m"
    bold_red = "\x1b[31;1m"
    yellow = "\x1b[33;20m"
    grey = "\x1b[38;20m"

    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def init_logger():
    global LOGGER
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())

    LOGGER.addHandler(ch)

init_logger()

def error(e):
    error_message = traceback.format_exc()
    # 使用 logger 打印异常信息
    LOGGER.error("An error occurred:\n%s", error_message)