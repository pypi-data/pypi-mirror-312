# arpakit

import asyncio
import inspect
import logging
from datetime import timedelta

import aiohttp
import requests

from arpakitlib.ar_safe_sleep import safe_sleep

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def sync_make_request(*, method: str, url: str, **kwargs) -> requests.Response:
    _logger = logging.getLogger(inspect.currentframe().f_code.co_name)

    max_tries = 7
    tries = 0

    kwargs["method"] = method
    kwargs["url"] = url
    if "timeout" not in kwargs:
        kwargs["timeout"] = (timedelta(seconds=15).total_seconds(), timedelta(seconds=15).total_seconds())

    while True:
        tries += 1
        _logger.info(f"{method} {url}")
        try:
            return requests.request(**kwargs)
        except Exception as err:
            _logger.warning(f"{tries}/{max_tries} {method} {url} {err}")
            if tries >= max_tries:
                raise Exception(err)
            safe_sleep(timedelta(seconds=0.1).total_seconds())
            continue


async def async_make_request(*, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
    _logger = logging.getLogger(inspect.currentframe().f_code.co_name)

    max_tries = 7
    tries = 0

    kwargs["method"] = method
    kwargs["url"] = url
    if "timeout" not in kwargs:
        kwargs["timeout"] = aiohttp.ClientTimeout(total=timedelta(seconds=15).total_seconds())

    while True:
        tries += 1
        _logger.info(f"{method} {url}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(**kwargs) as response:
                    await response.read()
                    return response
        except Exception as err:
            _logger.warning(f"{tries}/{max_tries} {method} {url} {err}")
            if tries >= max_tries:
                raise Exception(err)
            await asyncio.sleep(timedelta(seconds=0.1).total_seconds())
            continue


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
