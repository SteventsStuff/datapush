from sanic.response import json, text
from http import HTTPStatus
import aiohttp
import logging  # i will make full log config later


class BaseDomain:
    def __init__(self, url):
        self.url = url

    async def get_instances(self):
        async with aiohttp.request(
                method="GET", url=self.url
        ) as service_response:
            print(await service_response.json())
            result = await service_response.json()

        if service_response.status == HTTPStatus.OK:
            msg = f"Operation successful"
            logging.info(msg)
            return json(result)
        else:
            msg = "Can not make request, service is unavailable now"
            logging.error(msg)
            return text(f"Error: {msg}")

