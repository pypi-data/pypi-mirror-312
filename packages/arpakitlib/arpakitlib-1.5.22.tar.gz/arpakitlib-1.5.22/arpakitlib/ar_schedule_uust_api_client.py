# arpakit

import asyncio
import hashlib
import logging
from datetime import timedelta, datetime
from typing import Optional, Any

import aiohttp
import pytz
from aiohttp import ClientTimeout
from aiohttp_socks import ProxyConnector

from arpakitlib.ar_dict_util import combine_dicts

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class ScheduleUUSTAPIClient:
    def __init__(
            self,
            *,
            api_login: str,
            api_password: str | None = None,
            api_password_first_part: str | None = None,
            api_url: str = "https://isu.uust.ru/api/schedule_v2",
            api_proxy_url: str | None = None
    ):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.api_login = api_login
        self.api_password = api_password
        self.api_password_first_part = api_password_first_part
        self.api_url = api_url
        self.api_proxy_url = api_proxy_url
        self.headers = {
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;"
                "q=0.8,application/signed-exchange;v=b3;q=0.7"
            ),
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
            )
        }

    def auth_params(self) -> dict[str, Any]:
        if self.api_password:
            return {
                "login": self.api_login,
                "pass": self.api_password
            }
        elif self.api_password_first_part:
            return {
                "login": self.api_login,
                "pass": self.generate_v2_token(password_first_part=self.api_password_first_part)
            }
        else:
            return {}

    @classmethod
    def hash_token(cls, token: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(token.encode('utf-8'))
        return sha256.hexdigest()

    @classmethod
    def generate_v2_token(cls, password_first_part: str) -> str:
        return cls.hash_token(
            password_first_part + datetime.now(tz=pytz.timezone("Asia/Yekaterinburg")).strftime("%Y-%m-%d")
        )

    async def _async_get_request(
            self,
            *,
            url: str,
            params: Optional[dict] = None
    ) -> dict[str, Any]:
        max_tries = 7
        tries = 0

        while True:
            self._logger.info(f"GET {url} {params} proxy={self.api_proxy_url}")

            tries += 1

            connector = (
                ProxyConnector.from_url(self.api_proxy_url)
                if self.api_proxy_url is not None
                else None
            )

            try:
                async with aiohttp.ClientSession(connector=connector) as session:
                    async with session.get(
                            url=url,
                            params=params,
                            timeout=ClientTimeout(total=timedelta(seconds=15).total_seconds())
                    ) as response:
                        response.raise_for_status()
                        return await response.json()
            except Exception as err:
                self._logger.warning(f"{tries}/{max_tries} {err} GET {url} {params}  proxy={self.api_proxy_url}")
                if tries >= max_tries:
                    raise err
                await asyncio.sleep(timedelta(seconds=1).total_seconds())
                self._logger.warning(f"{tries}/{max_tries} AGAIN GET {url} {params}  proxy={self.api_proxy_url}")
                continue

    async def get_current_week(self) -> int:
        """
        response.json example
        {
            'data': [15]
        }
        """

        params = combine_dicts(self.auth_params(), {"ask": "get_current_week"})
        json_data = await self._async_get_request(
            url=self.api_url,
            params=params
        )
        return json_data["data"][0]

    async def get_current_semester(self) -> str:
        """
        response.json example
        {
            'data': ['Осенний семестр 2023/2024']
        }
        """

        params = combine_dicts(self.auth_params(), {"ask": "get_current_semestr"})
        json_data = await self._async_get_request(
            url=self.api_url,
            params=params
        )
        return json_data["data"][0]

    async def get_groups(self) -> list[dict[str, Any]]:
        """
        response.json example
        {
            "data": {
                "4438": {
                    "group_id": 4438,
                    "group_title": "АРКТ-101А",
                    "faculty": "",
                    "course": 1
                }
            }
        }
        """

        params = combine_dicts(self.auth_params(), {"ask": "get_group_list"})
        json_data = await self._async_get_request(
            url=self.api_url,
            params=params
        )
        return list(json_data["data"].values())

    async def get_group_lessons(self, group_id: int, semester: str | None = None) -> list[dict[str, Any]]:
        params = combine_dicts(
            self.auth_params(),
            {
                "ask": "get_group_schedule",
                "id": group_id
            }
        )
        if semester is not None:
            params["semester"] = semester
        json_data = await self._async_get_request(
            url=self.api_url,
            params=params
        )
        return json_data["data"]

    async def get_teachers(self) -> list[dict[str, Any]]:
        params = combine_dicts(self.auth_params(), {"ask": "get_teacher_list"})
        json_data = await self._async_get_request(
            url=self.api_url,
            params=params
        )
        return list(json_data["data"].values())

    async def get_teacher_lessons(self, teacher_id: int, semester: str | None = None) -> list[dict[str, Any]]:
        params = combine_dicts(self.auth_params(), {"ask": "get_teacher_schedule", "id": teacher_id})
        if semester is not None:
            params["semester"] = semester
        json_data = await self._async_get_request(
            url=self.api_url,
            params=params
        )
        return json_data["data"]

    async def check_conn(self):
        await self.get_current_week()

    async def is_conn_good(self):
        try:
            await self.check_conn()
        except Exception as e:
            self._logger.error(e)
            return False
        return True


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
