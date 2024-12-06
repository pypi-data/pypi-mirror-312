# arpakit

import logging
import math
from time import sleep

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


def safe_sleep(sleep_time: float | int):
    _logger.info(f"sleep_time={sleep_time}")
    frac, int_part = math.modf(sleep_time)
    for i in range(int(int_part)):
        sleep(1)
    sleep(frac)


def __example():
    pass


if __name__ == '__main__':
    __example()
