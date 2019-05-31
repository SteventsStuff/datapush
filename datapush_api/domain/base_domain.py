from sanic.response import json, text
from http import HTTPStatus
import aiohttp
import logging  # i will make full log config later


class BaseDomain:
    def __init__(self, url, params=None):
        self.url = url
        self.params = params

    async def get_instances(self):
        print("params", self.params)

        async with aiohttp.request(
            method="GET", url=self.url, params=self.params
        ) as service_response:
            result = await service_response.json()

        if service_response.status == HTTPStatus.OK:
            msg = f"Operation successful"
            logging.info(msg)
            return json(result)
        else:
            msg = "Can not make request, service is unavailable now"
            logging.error(msg)
            return json({"Error": msg})

    async def get_instance_by_key(self):
        if len(self.params.keys()) == 1 and list(self.params.keys())[0] == "id":
            return await self.get_instances()
        else:
            return text("You must use only ID parameter!")

    async def get_instances_by_filters(self):
        pass
