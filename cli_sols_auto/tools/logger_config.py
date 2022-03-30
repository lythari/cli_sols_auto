import logging
import sys

import colorlog

logger: logging.Logger = logging.getLogger(__name__)
formatter: logging.Formatter = colorlog.ColoredFormatter("%(asctime)s [%(bold)s%(name)s%(reset)s:%(threadName)s] "
                                                         "%(log_color)s%(levelname)-8s%(reset)s %(message)s "
                                                         "(%(bold)s%(filename)s%(reset)s:%(funcName)s:%(lineno)d)")
console_handler: logging.Handler = colorlog.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
