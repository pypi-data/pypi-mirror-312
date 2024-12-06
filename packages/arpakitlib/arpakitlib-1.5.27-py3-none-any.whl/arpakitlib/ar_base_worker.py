# arpakit

import asyncio
import logging
from abc import ABC
from datetime import timedelta
from typing import Any

from arpakitlib.ar_safe_sleep import safe_sleep

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class BaseWorker(ABC):

    def __init__(self):
        self.worker_name = self.__class__.__name__
        self._logger = logging.getLogger(self.worker_name)
        self.timeout_after_run: float | None = timedelta(seconds=15).total_seconds()
        self.timeout_after_err_in_run: float | None = timedelta(seconds=15).total_seconds()

    def sync_on_startup(self):
        pass

    def sync_run(self):
        raise NotImplementedError()

    def sync_run_on_error(self, exception: BaseException, kwargs: dict[str, Any]):
        self._logger.exception(exception)

    def sync_safe_run(self):
        self._logger.info(f"sync_safe_run")

        self._logger.info("sync_on_startup starts")
        self.sync_on_startup()
        self._logger.info("sync_on_startup ends")

        while True:

            try:

                self._logger.info("sync_run starts")
                self.sync_run()
                self._logger.info("sync_run ends")

                if self.timeout_after_run is not None:
                    safe_sleep(self.timeout_after_run)

            except BaseException as exception:

                self._logger.info("sync_run_on_error starts")
                self.sync_run_on_error(exception=exception, kwargs={})
                self._logger.info("sync_run_on_error ends")

                if self.timeout_after_err_in_run is not None:
                    safe_sleep(self.timeout_after_err_in_run)

    async def async_on_startup(self):
        pass

    async def async_run(self):
        raise NotImplementedError()

    async def async_run_on_error(self, exception: BaseException, kwargs: dict[str, Any]):
        self._logger.exception(exception)

    async def async_safe_run(self):
        self._logger.info(f"async_safe_run starts")

        self._logger.info("async_on_startup starts")
        await self.async_on_startup()
        self._logger.info("async_on_startup ends")

        while True:

            try:

                await self.async_run()

                if self.timeout_after_run is not None:
                    await asyncio.sleep(self.timeout_after_run)

            except BaseException as exception:

                self._logger.info("async_run_on_error starts")
                await self.async_run_on_error(exception=exception, kwargs={})
                self._logger.info("async_run_on_error ends")

                if self.timeout_after_err_in_run is not None:
                    await asyncio.sleep(self.timeout_after_err_in_run)


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
